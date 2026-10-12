from venv import create
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from streamlit import success
from .models import Course, Module, Enrollment, Feedback, EnrollmentNotification, ModuleNotification, Like
from .forms import CourseForm, ModuleForm, FeedbackForm
from django.contrib import messages
from rest_framework import generics, permissions
from .serializers import CourseSerializer
from django.utils.text import slugify
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# like functions
# get likes
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_likes(request):
    #Get all courses liked by the current user#
    liked_courses = Like.objects.filter(
        student=request.user
    ).values_list('course_id', flat=True)
    return Response(list(liked_courses))

# toggle likes
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def toggle_like(request, course_id):
    #Toggle like status for a course#
    course = get_object_or_404(Course, id=course_id)
    like, created = Like.objects.get_or_create(
        student=request.user,
        course=course,
        defaults={'student': request.user, 'course': course}
    )
    
    if not created:
        # Like already exists, so unlike it
        like.delete()
        liked = False
    else:
        liked = True
    
    # Get updated like count
    like_count = Like.objects.filter(course=course).count()
    
    return Response({
        'liked': liked,
        'like_count': like_count
    })

# Courses
# course list
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add notifications for teachers
        if self.request.user.is_authenticated and self.request.user.is_teacher:
            context['notifications'] = EnrollmentNotification.objects.filter(
                teacher=self.request.user,
            ).order_by('-created_at')[:10]  # Show last 10 unread notifications


        #  Add module notifications for students
        if self.request.user.is_authenticated and self.request.user.is_student:
            context['module_notifications'] = ModuleNotification.objects.filter(
                student=self.request.user,
            ).order_by('-created_at')[:10]

                # Add initial like data for authenticated users
        if self.request.user.is_authenticated:
            liked_courses = Like.objects.filter(
                student=self.request.user
            ).values_list('course_id', flat=True)
            context['user_likes'] = list(liked_courses)
        else:
            context['user_likes'] = []
        
        return context
    
# course detail
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrolled'] = False
        user_feedback_exists = False
        # check whether student is enrolled
        if self.request.user.is_authenticated:
            context['enrolled'] = Enrollment.objects.filter(
                student=self.request.user,
                course=self.object).exists()
            # show existing feedback data from enrolled students
            user_feedback_exists = Feedback.objects.filter(
                course=self.object,
                student=self.request.user
            ).exists()
        # add the list of enrolled students for the teachers only
        if self.request.user == self.object.teacher:
            context['enrolled_students'] = self.object.students.all().order_by('username')
    
        context['user_feedback_exists'] = user_feedback_exists
        return context

# course create
class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_teacher

# course update
class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    
    def test_func(self):
        course = self.get_object()
        return self.request.user == course.teacher

# course delete
class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'courses/course_delete.html'
    success_url = reverse_lazy('course_list')
    
    def test_func(self):
        course = self.get_object()
        return self.request.user == course.teacher

# enroll course
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.is_authenticated and not Enrollment.objects.filter(student=request.user, course=course).exists():
        # add student to course database
        course.students.add(request.user)
        Enrollment.objects.create(student=request.user, course=course)
        
        # notification for teachers
        EnrollmentNotification.objects.create(
            teacher=course.teacher,
            course=course,
            student=request.user,
            message=f"{request.user.username} has enrolled in your course '{course.title}'"
        )

        messages.success(request, f'You have successfully enrolled in {course.title}')
    return redirect('course_detail', slug=course.slug)

#  delete notifications
@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(EnrollmentNotification, id=notification_id, teacher=request.user)
    notification.delete()
    messages.success(request, 'Notification deleted successfully.')
    return redirect('course_list')

# remove student from course
@login_required
def remove_student(request, course_slug, student_id):
    course = get_object_or_404(Course, slug=course_slug)
    student = get_object_or_404(CustomUser, id=student_id)
    
    # check if the current user is the course teacher
    if request.user != course.teacher:
        return HttpResponseForbidden("You are not authorized to remove students from this course")
    
    # remove the student from the course
    if course.students.filter(id=student_id).exists():
        course.students.remove(student)    

        # delete enrollment data
        Enrollment.objects.filter(course=course, student=student).delete()

        # delete any feedback from this student
        Feedback.objects.filter(course=course, student=student).delete()
        messages.success(request, f'{student.username} has been removed from this course')
    return redirect('course_detail', slug=course_slug)

# course lsit api
class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# course detail api
class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

# submit feedback function
@login_required
def submit_feedback(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        return HttpResponseForbidden("You must be enrolled in this course to leave feedback")
    # check if users laready exists in databse
    feedback_exists = Feedback.objects.filter(course=course, student=request.user).exists()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            if feedback_exists:
                # Update existing feedback
                feedback = Feedback.objects.get(course=course, student=request.user)
                feedback.comment = form.cleaned_data['comment']
                feedback.save()
                messages.success(request, 'Your feedback has been updated!')
            else:
                #create and save new feedback, linking it to the course and student
                feedback = form.save(commit=False)
                feedback.course = course
                feedback.student = request.user
                feedback.save()
                messages.success(request, 'Thank you for your feedback!')
            return redirect('course_detail', slug=course.slug)
    else:
        # GET request: Pre-populate the form if updating, show empty form if creating
        if feedback_exists:
            feedback = Feedback.objects.get(course=course, student=request.user)
            form = FeedbackForm(instance=feedback)
        else:
            form = FeedbackForm()
    # render the form template
    return render(request, 'courses/course_feedback.html', {
        'form': form,
        'course': course,
        'feedback_exists': feedback_exists
    })

###### Modules######
# module create
class ModuleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = 'courses/module_form.html'
    # get course
    def get_course(self): 
        return get_object_or_404(Course, slug=self.kwargs['course_slug'])
    # form
    def form_valid(self, form): 
        form.instance.course = self.get_course() 
        result = super().form_valid(form)  # Store the result first
        
        # Create notifications for all enrolled students
        course = self.get_course()
        enrolled_students = course.students.all()

        # module notification for student
        for student in enrolled_students:
            ModuleNotification.objects.create(
                student=student,
                course=course,
                module=self.object,
                message=f"New module '{self.object.title}' added to course '{course.title}'"
            )
        
        return result  # Return the result after creating notifications

    # success url
    def get_success_url(self):
        return reverse('course_detail', kwargs={'slug': self.get_course().slug})
    
    # context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.get_course()
        return context
        
    #  test function
    def test_func(self): 
        course = self.get_course() 
        return self.request.user == course.teacher
    
# to delete notification module
@login_required
def delete_module_notification(request, notification_id):
    notification = get_object_or_404(ModuleNotification, id=notification_id, student=request.user)
    notification.delete()
    messages.success(request, 'Notification deleted successfully.')
    return redirect('course_list')

# module update
class ModuleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Module 
    form_class = ModuleForm 
    template_name = 'courses/module_form.html' 
    
    def get_success_url(self): 
        return reverse('course_detail', kwargs={'slug': self.object.course.slug}) 
    
    def test_func(self): 
        module = self.get_object() 
        return self.request.user == module.course.teacher

# module delete
class ModuleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): 
    model = Module 
    template_name = 'courses/module_delete.html' 
    
    def get_success_url(self): 
        return reverse('course_detail', kwargs={'slug': self.object.course.slug}) 
    
    def test_func(self): 
        module = self.get_object() 
        return self.request.user == module.course.teacher