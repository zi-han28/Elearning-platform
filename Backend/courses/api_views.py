from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import Course, Module, Enrollment, Feedback, EnrollmentNotification, ModuleNotification, Like
from .forms import CourseForm, ModuleForm, FeedbackForm
from django.contrib import messages
from rest_framework import generics, permissions
from .serializers import (
    CourseSerializer,
    CourseListSerializer,
    ModuleSerializer,
    FeedbackSerializer,
    EnrollmentNotificationSerializer,
    ModuleNotificationSerializer,
)
from .permissions import IsTeacher, IsCourseTeacherOrReadOnly, IsCourseTeacher
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
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


# course list + create api
class CourseListAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.select_related("teacher").prefetch_related("likes")
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        return CourseSerializer if self.request.method == "POST" else CourseListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsTeacher()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

# course detail / update / delete api
class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.select_related("teacher").prefetch_related("modules", "feedbacks__student", "likes")
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCourseTeacherOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = 'slug'


class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacher]  # = LoginRequiredMixin + test_func(is_teacher)
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class CourseUpdateAPIView(generics.UpdateAPIView):
    queryset = Course.objects.select_related("teacher")
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseTeacher]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

# enroll course api
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def enroll_course_api(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        return Response({"detail": "Already enrolled."}, status=status.HTTP_400_BAD_REQUEST)

    course.students.add(request.user)
    Enrollment.objects.create(student=request.user, course=course)
    EnrollmentNotification.objects.create(
        teacher=course.teacher,
        course=course,
        student=request.user,
        message=f"{request.user.username} has enrolled in your course '{course.title}'"
    )
    return Response({"detail": f"You have successfully enrolled in {course.title}"}, status=status.HTTP_201_CREATED)

# remove student api
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_student_api(request, course_slug, student_id):
    course = get_object_or_404(Course, slug=course_slug)
    if request.user != course.teacher:
        return Response({"detail": "You are not authorized to remove students from this course"}, status=status.HTTP_403_FORBIDDEN)

    student = get_object_or_404(CustomUser, id=student_id)
    if not course.students.filter(id=student_id).exists():
        return Response({"detail": "Student is not enrolled in this course."}, status=status.HTTP_404_NOT_FOUND)

    course.students.remove(student)
    Enrollment.objects.filter(course=course, student=student).delete()
    Feedback.objects.filter(course=course, student=student).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# feedback api: GET own feedback, POST creates or updates it
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def feedback_api(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        return Response({"detail": "You must be enrolled in this course to leave feedback"}, status=status.HTTP_403_FORBIDDEN)

    feedback = Feedback.objects.filter(course=course, student=request.user).first()
    if request.method == 'GET':
        if not feedback:
            return Response({"detail": "No feedback yet."}, status=status.HTTP_404_NOT_FOUND)
        return Response(FeedbackSerializer(feedback).data)

    serializer = FeedbackSerializer(feedback, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(course=course, student=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK if feedback else status.HTTP_201_CREATED)

# module list + create api
class ModuleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_course(self):
        return get_object_or_404(Course, slug=self.kwargs['course_slug'])

    def get_queryset(self):
        return Module.objects.filter(course__slug=self.kwargs['course_slug'])

    def perform_create(self, serializer):
        course = self.get_course()
        if self.request.user != course.teacher:
            raise PermissionDenied("Only the course teacher can add modules.")
        module = serializer.save(course=course)

        # module notification for enrolled students
        ModuleNotification.objects.bulk_create([
            ModuleNotification(
                student=student,
                course=course,
                module=module,
                message=f"New module '{module.title}' added to course '{course.title}'"
            )
            for student in course.students.all()
        ])

# module detail / update / delete api
class ModuleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.select_related("course")
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCourseTeacherOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

# notifications api: enrollment notices for teachers, module notices for students
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notifications_api(request):
    data = {"enrollment_notifications": [], "module_notifications": []}
    if request.user.is_teacher:
        qs = EnrollmentNotification.objects.filter(teacher=request.user)[:10]
        data["enrollment_notifications"] = EnrollmentNotificationSerializer(qs, many=True).data
    if request.user.is_student:
        qs = ModuleNotification.objects.filter(student=request.user)[:10]
        data["module_notifications"] = ModuleNotificationSerializer(qs, many=True).data
    return Response(data)

class EnrollmentNotificationDeleteAPIView(generics.DestroyAPIView):
    def get_queryset(self):
        return EnrollmentNotification.objects.filter(teacher=self.request.user)

class ModuleNotificationDeleteAPIView(generics.DestroyAPIView):
    def get_queryset(self):
        return ModuleNotification.objects.filter(student=self.request.user)