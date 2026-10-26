from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CreateUserView, CustomTokenView,
    MyProfileView, UserSearchView, UserDetailView,
)

urlpatterns = [
    path('user/register/', CreateUserView.as_view(), name='api_register'),
    path('token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', MyProfileView.as_view(), name='api_profile'),
    path('users/search/', UserSearchView.as_view(), name='api_user_search'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='api_user_detail'),
]