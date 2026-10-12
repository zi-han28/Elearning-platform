from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from .models import Course, Module, Enrollment, Feedback, EnrollmentNotification, ModuleNotification
from .forms import CourseForm, ModuleForm, FeedbackForm
from users.models import CustomUser

User = get_user_model()

class CourseModelTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='testpass123',
            is_teacher=True
        )
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='testpass123',
            is_student=True
        )
        
    def test_course_creation(self):
        #Test creating a course#
        course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            teacher=self.teacher,
            overview='Test course overview'
        )
        
        self.assertEqual(course.title, 'Test Course')
        self.assertEqual(course.slug, 'test-course')
        self.assertEqual(course.teacher, self.teacher)
        self.assertEqual(course.overview, 'Test course overview')
        
    def test_course_str_representation(self):
        #Test course string representation#
        course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            teacher=self.teacher,
            overview='Test course overview'
        )
        self.assertEqual(str(course), 'Test Course')
        
    def test_course_get_absolute_url(self):
        #Test course get_absolute_url method#
        course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            teacher=self.teacher,
            overview='Test course overview'
        )
        expected_url = reverse('course_detail', args=[course.slug])
        self.assertEqual(course.get_absolute_url(), expected_url)
        
    def test_course_get_course_picture_url(self):
        #Test course picture URL method#
        course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            teacher=self.teacher,
            overview='Test course overview'
        )
        # Test default URL
        self.assertEqual(course.get_course_picture_url(), '/media/course_pics/default.jpg')

class ModuleModelTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='testpass123',
            is_teacher=True
        )
        self.course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            teacher=self.teacher,
            overview='Test course overview'
        )
        
    def test_module_creation(self):
        #Test creating a module#
        module = Module.objects.create(
            course=self.course,
            title='Test Module',
            description='Test module description',
            order=1
        )
        
        self.assertEqual(module.title, 'Test Module')
        self.assertEqual(module.course, self.course)
        self.assertEqual(module.order, 1)
        
    def test_module_str_representation(self):
        #Test module string representation#
        module = Module.objects.create(
            course=self.course,
            title='Test Module',
            order=1
        )
        self.assertEqual(str(module), '1. Test Module')
        
    def test_module_ordering(self):
        #Test module ordering#
        module2 = Module.objects.create(course=self.course, title='Module 2', order=2)
        module1 = Module.objects.create(course=self.course, title='Module 1', order=1)
        
        modules = Module.objects.all()
        self.assertEqual(modules[0], module1)
        self.assertEqual(modules[1], module2)

class EnrollmentModelTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='testpass123',
            is_teacher=True
        )
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='testpass123',
            is_student=True
        )
        self.course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            teacher=self.teacher,
            overview='Test course overview'
        )
        
    def test_enrollment_creation(self):
        #Test creating an enrollment#
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course
        )
        
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.course, self.course)
        
    def test_enrollment_unique_together(self):
        #Test that a student can't enroll in the same course twice#
        Enrollment.objects.create(student=self.student, course=self.course)
        
        with self.assertRaises(ValidationError):
            enrollment2 = Enrollment(student=self.student, course=self.course)
            enrollment2.full_clean()  # This should raise ValidationError
            
    def test_enrollment_str_representation(self):
        #Test enrollment string representation#
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course
        )
        expected_str = f"{self.student.username} enrolled in {self.course.title}"
        self.assertEqual(str(enrollment), expected_str)

class NotificationModelTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='testpass123',
            is_teacher=True
        )
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='testpass123',
            is_student=True
        )
        self.course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            teacher=self.teacher,
            overview='Test course overview'
        )
        
    def test_enrollment_notification_creation(self):
        #Test creating an enrollment notification#
        notification = EnrollmentNotification.objects.create(
            teacher=self.teacher,
            course=self.course,
            student=self.student,
            message='Test notification message'
        )
        
        self.assertEqual(notification.teacher, self.teacher)
        self.assertEqual(notification.course, self.course)
        self.assertEqual(notification.student, self.student)
        self.assertEqual(notification.message, 'Test notification message')
        
    def test_module_notification_creation(self):
        #Test creating a module notification#
        module = Module.objects.create(
            course=self.course,
            title='Test Module',
            order=1
        )
        
        notification = ModuleNotification.objects.create(
            student=self.student,
            course=self.course,
            module=module,
            message='Test module notification'
        )
        
        self.assertEqual(notification.student, self.student)
        self.assertEqual(notification.course, self.course)
        self.assertEqual(notification.module, module)
        self.assertEqual(notification.message, 'Test module notification')

class CourseFormTests(TestCase):
    def test_valid_course_form(self):
        #Test valid course form data#
        form_data = {
            'title': 'Test Course',
            'overview': 'Test course overview'
        }
        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_course_form(self):
        #Test invalid course form data#
        form_data = {
            'title': '',  # Required field
            'overview': 'Test course overview'
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

class ModuleFormTests(TestCase):
    def test_valid_module_form(self):
        #Test valid module form data#
        form_data = {
            'title': 'Test Module',
            'description': 'Test module description',
            'order': 1
        }
        form = ModuleForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_module_form(self):
        #Test invalid module form data#
        form_data = {
            'title': '',  # Required field
            'order': 0  # Should be at least 1
        }
        form = ModuleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

class FeedbackFormTests(TestCase):
    def test_valid_feedback_form(self):
        #Test valid feedback form data#
        form_data = {
            'comment': 'Great course!'
        }
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

class CourseViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='testpass123',
            is_teacher=True
        )
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='testpass123',
            is_student=True
        )
        self.course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            teacher=self.teacher,
            overview='Test course overview'
        )
        
    def test_course_list_view(self):
        #Test course list view#
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_list.html')
        self.assertContains(response, 'Test Course')
        
    def test_course_detail_view(self):
        #Test course detail view#
        response = self.client.get(reverse('course_detail', args=[self.course.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_detail.html')
        self.assertContains(response, 'Test Course')
        
    def test_course_create_view_authenticated_teacher(self):
        #Test course creation by authenticated teacher#
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('course_create'))
        self.assertEqual(response.status_code, 200)
        
    def test_course_create_view_authenticated_student(self):
        #Test course creation by authenticated student (should be forbidden)#
        self.client.login(username='student', password='testpass123')
        response = self.client.get(reverse('course_create'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
    def test_enroll_course_authenticated(self):
        #Test course enrollment by authenticated student#
        self.client.login(username='student', password='testpass123')
        response = self.client.post(reverse('enroll_course', args=[self.course.pk]))
        
        # Should redirect to course detail
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enrollment.objects.filter(student=self.student, course=self.course).exists())
        


class ModuleViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='testpass123',
            is_teacher=True
        )
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='testpass123',
            is_student=True
        )
        self.course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            teacher=self.teacher,
            overview='Test course overview'
        )
        
    def test_module_create_view_authenticated_teacher(self):
        #Test module creation by course teacher#
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('module_create', args=[self.course.slug]))
        self.assertEqual(response.status_code, 200)
        
    def test_module_create_view_authenticated_student(self):
        #Test module creation by student (should be forbidden)#
        self.client.login(username='student', password='testpass123')
        response = self.client.get(reverse('module_create', args=[self.course.slug]))
        self.assertEqual(response.status_code, 403)  # Forbidden

class NotificationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='testpass123',
            is_teacher=True
        )
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='testpass123',
            is_student=True
        )
        self.course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            teacher=self.teacher,
            overview='Test course overview'
        )
        self.enrollment_notification = EnrollmentNotification.objects.create(
            teacher=self.teacher,
            course=self.course,
            student=self.student,
            message='Test enrollment notification'
        )
        
    def test_delete_enrollment_notification_authenticated_teacher(self):
        #Test deleting enrollment notification by teacher#
        self.client.login(username='teacher', password='testpass123')
        response = self.client.post(reverse('delete_notification', args=[self.enrollment_notification.id]))
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertFalse(EnrollmentNotification.objects.filter(id=self.enrollment_notification.id).exists())
        

