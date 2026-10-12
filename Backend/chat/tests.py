from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course
from .models import ChatMessage
from django.utils import timezone

User = get_user_model()

class ChatAppTests(TestCase):
    def setUp(self):
        #Set up test data#
        # Create users
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
        
        # Create a course
        self.course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            teacher=self.teacher,
            overview='Test course overview'
        )
        
        # Enroll student in course
        self.course.students.add(self.student)
        
        # Create some test messages
        self.message1 = ChatMessage.objects.create(
            course=self.course,
            user=self.teacher,
            message='Hello students!',
            timestamp=timezone.now()
        )
        self.message2 = ChatMessage.objects.create(
            course=self.course,
            user=self.student,
            message='Hello teacher!',
            timestamp=timezone.now()
        )
        
        self.client = Client()

    def test_chat_room_view_authenticated(self):
        #Test that authenticated users can access chat room#
        # Login as student
        self.client.login(username='student', password='testpass123')
        
        response = self.client.get(reverse('chat_room', args=[self.course.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/room.html')
        self.assertContains(response, 'Hello students!')
        self.assertContains(response, 'Hello teacher!')

    def test_chat_message_creation(self):
        #Test that chat messages can be created#
        message = ChatMessage.objects.create(
            course=self.course,
            user=self.student,
            message='Test message',
            timestamp=timezone.now()
        )
        
        self.assertEqual(ChatMessage.objects.count(), 3)
        self.assertEqual(message.message, 'Test message')
        self.assertEqual(message.user, self.student)
        self.assertEqual(message.course, self.course)

    def test_chat_message_ordering(self):
        #Test that messages are ordered by timestamp#
        messages = ChatMessage.objects.all()
        self.assertEqual(messages[0], self.message1)
        self.assertEqual(messages[1], self.message2)
        
    def test_chat_message_str_representation(self):
        #Test the string representation of chat messages#
        self.assertEqual(
            str(self.message1),
            f"{self.teacher.username}: {self.message1.message[:20]}..."
        )

    def test_chat_room_context_data(self):
        #Test that chat room view passes correct context data#
        self.client.login(username='student', password='testpass123')
        
        response = self.client.get(reverse('chat_room', args=[self.course.slug]))
        
        # Check context data
        self.assertEqual(response.context['course'], self.course)
        self.assertEqual(response.context['username'], 'student')
        
        # Check initial messages
        initial_messages = response.context['initial_messages']
        self.assertEqual(len(initial_messages), 2)
        self.assertIn(self.message1, initial_messages)
        self.assertIn(self.message2, initial_messages)