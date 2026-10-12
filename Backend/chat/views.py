from django.shortcuts import render, get_object_or_404
from courses.models import Course
from django.contrib.auth.decorators import login_required
from .models import ChatMessage

@login_required
def chat_room(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    messages = ChatMessage.objects.filter(course=course).order_by('timestamp')[:50]
    return render(request, 'chat/room.html', {
        'course': course,
        'username': request.user.username,
        'initial_messages': messages 
    })