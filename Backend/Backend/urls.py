#Backend/urls.py
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views 
from users.views import CreateUserView, CustomTokenView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.api_urls')),
    path('api/user/register/', CreateUserView.as_view(), name='api_register'),
    path('api/token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include("rest_framework.urls")),



    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',extra_context={'title': 'Login'}, redirect_authenticated_user = True, next_page='profile'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html',extra_context={'title': 'Logout'}, next_page = 'login'), name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('', include('courses.urls')),
    path('chat/', include('chat.urls')),
    path('users/', include('users.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)