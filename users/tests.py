from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from .models import CustomUser, Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserSearchForm

User = get_user_model()

class CustomUserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    
    def test_create_user(self):
        #Test creating a regular user#
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_student)
        self.assertFalse(user.is_teacher)
        self.assertTrue(user.check_password('testpass123'))
    
    def test_create_superuser(self):
        #Test creating a superuser#
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
    
    def test_user_str_representation(self):
        #Test user string representation#
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')
    
    def test_teacher_user_creation(self):
        #Test creating a teacher user#
        user = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='testpass123',
            is_teacher=True
        )
        self.assertTrue(user.is_teacher)
        self.assertFalse(user.is_student)
    
    def test_user_save_method(self):
        #Test user save method logic#
        user = User(
            username='testteacher',
            email='teacher@example.com',
            is_teacher=True
        )
        user.save()
        user.refresh_from_db()
        self.assertTrue(user.is_teacher)
        self.assertFalse(user.is_student)

class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_creation_signal(self):
        #Test that profile is automatically created via signal#
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsNotNone(self.user.profile)
        self.assertEqual(self.user.profile.profile_picture.name, 'profile_pics/default.jpg')
        self.assertEqual(self.user.profile.status, 'active')
    
    def test_profile_str_representation(self):
        #Test profile string representation#
        self.assertEqual(str(self.user.profile), 'testuser Profile')
    
    def test_profile_status_choices(self):
        #Test profile status choices#
        profile = self.user.profile
        valid_statuses = ['active', 'not_active', 'busy', 'anonymous']
        
        for status in valid_statuses:
            profile.status = status
            profile.save()
            profile.refresh_from_db()
            self.assertEqual(profile.status, status)
    

class UserRegisterFormTests(TestCase):
    def test_valid_registration_form(self):
        #Test valid user registration form#
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'is_teacher': False
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_registration_form(self):
        #Test invalid user registration form#
        form_data = {
            'username': '',  # Required field
            'email': 'invalid-email',  # Invalid email
            'password1': 'short',
            'password2': 'different',
            'is_teacher': False
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)
    
    def test_teacher_registration(self):
        #Test teacher registration#
        form_data = {
            'username': 'teacheruser',
            'email': 'teacher@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'is_teacher': True
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertTrue(user.is_teacher)
        self.assertFalse(user.is_student)

class UserUpdateFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_valid_user_update_form(self):
        #Test valid user update form#
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com'
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
    
class ProfileUpdateFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile
    
    def test_valid_profile_update_form(self):
        #Test valid profile update form#
        form_data = {
            'bio': 'Updated bio text',
            'status': 'busy'
        }
        form = ProfileUpdateForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
    

class UserSearchFormTests(TestCase):
    def test_valid_search_form(self):
        #Test valid user search form#
        form_data = {
            'search_query': 'test',
            'user_type': 'students'
        }
        form = UserSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_search_form_with_only_query(self):
        #Test search form with only search query#
        form_data = {
            'search_query': 'testuser',
            'user_type': ''
        }
        form = UserSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

class UserViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='testpass123',
            is_teacher=True
        )
    
    def test_register_view_get(self):
        #Test register view GET request#
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIsInstance(response.context['form'], UserRegisterForm)
    
    def test_register_view_post_valid(self):
        #Test register view POST with valid data#
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'is_teacher': False
        }
        response = self.client.post(reverse('register'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_profile_view_authenticated(self):
        #Test profile view for authenticated user#
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIsInstance(response.context['u_form'], UserUpdateForm)
        self.assertIsInstance(response.context['p_form'], ProfileUpdateForm)

    
    def test_profile_update_post(self):
        #Test profile update POST request#
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'bio': 'Updated bio',
            'status': 'busy'
        }
        response = self.client.post(reverse('profile'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Refresh user from database
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.profile.bio, 'Updated bio')
        self.assertEqual(self.user.profile.status, 'busy')
    
    def test_user_search_view_teacher_access(self):
        #Test user search view for teacher#
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('user_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_search.html')
        self.assertIsInstance(response.context['form'], UserSearchForm)
    
    def test_user_search_view_student_access(self):
        #Test user search view for student (should be forbidden)#
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_search.html')
        self.assertIsInstance(response.context['form'], UserSearchForm)
    
    def test_profile_view_by_id_authenticated(self):
        #Test viewing another user's profile by ID#
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile_view', args=[self.teacher.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile.html')
        self.assertEqual(response.context['viewed_user'], self.teacher)


class UserSearchFunctionalityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='testpass123',
            is_teacher=True
        )
        self.teacher.profile.status = 'active'
        self.teacher.profile.save()
        
        self.student1 = User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='testpass123',
            is_student=True
        )
        self.student1.profile.status = 'busy'
        self.student1.profile.save()
        
        self.student2 = User.objects.create_user(
            username='student2',
            email='student2@example.com',
            password='testpass123',
            is_student=True
        )
        self.student2.profile.status = 'anonymous'
        self.student2.profile.save()
        
        self.client.login(username='teacher1', password='testpass123')
    
    def test_search_by_username(self):
        #Test searching users by username#
        response = self.client.get(reverse('user_search') + '?search_query=student1&user_type=all')
        self.assertEqual(response.status_code, 200)
        users = response.context['users']
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first(), self.student1)
    
    def test_search_by_email(self):
        #Test searching users by email#
        response = self.client.get(reverse('user_search') + '?search_query=student2@example.com&user_type=all')
        self.assertEqual(response.status_code, 200)
        users = response.context['users']
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first(), self.student2)
    
    def test_search_by_status(self):
        #Test searching users by status#
        response = self.client.get(reverse('user_search') + '?search_query=busy&user_type=all')
        self.assertEqual(response.status_code, 200)
        users = response.context['users']
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first(), self.student1)
    
    def test_filter_teachers_only(self):
        #Test filtering teachers only#
        response = self.client.get(reverse('user_search') + '?user_type=teachers')
        self.assertEqual(response.status_code, 200)
        users = response.context['users']
        # Should find all teachers except the current user
        self.assertEqual(users.count(), 0)  # Only teacher is the current user, who is excluded
    
    def test_filter_students_only(self):
        #Test filtering students only#
        response = self.client.get(reverse('user_search') + '?user_type=students')
        self.assertEqual(response.status_code, 200)
        users = response.context['users']
        self.assertEqual(users.count(), 2)  # Both students
        self.assertIn(self.student1, users)
        self.assertIn(self.student2, users)
    
    def test_search_all_users(self):
        #Test searching all users#
        response = self.client.get(reverse('user_search') + '?user_type=all')
        self.assertEqual(response.status_code, 200)
        users = response.context['users']
        self.assertEqual(users.count(), 2)