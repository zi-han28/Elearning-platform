# users/urls.py
from django.urls import path
from . import views
from .views import MyProfileView, UserSearchView, UserDetailView, CustomTokenView

urlpatterns = [
    path('api/profile', MyProfileView.as_view(), name='api_profile'),
    path('api/users/search/', UserSearchView.as_view(), name='api_user_search'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='api_user_detail'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.user_search, name='user_search'),
    path('profile/<int:user_id>/', views.profile_view, name='profile_view'),
]
