from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.user_search, name='user_search'),
    path('profile/<int:user_id>/', views.profile_view, name='profile_view'),
]