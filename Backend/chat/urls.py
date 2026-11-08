from django.urls import path
from . import views
from .views import ChatHistoryAPIView

urlpatterns = [
    path('<slug:course_slug>/', views.chat_room, name='chat_room'),
    path('api/<slug:course_slug>/messages/', ChatHistoryAPIView.as_view(), name='api_chat_room')
]