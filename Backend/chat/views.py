from django.shortcuts import render, get_object_or_404
from courses.models import Course
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from rest_framework import generics, permissions
from .serializers import ChatMessageSerializer


# django tempate
@login_required
def chat_room(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)

    # oldest 50 messages
    # messages = ChatMessage.objects.filter(course=course).order_by('timestamp')[:50]

    messages = list(ChatMessage.objects.filter(course=course).select_related('user'))
    return render(request, 'chat/room.html', {
        'course': course,
        'username': request.user.username,
        'initial_messages': messages 
    })


# React template
class ChatHistoryAPIView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        messages = (ChatMessage.objects.filter(course__slug=self.kwargs["course_slug"]).select_related('user'))
        return list(messages)