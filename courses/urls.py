from django.urls import path
from .views import (
    CourseListView, 
    CourseDetailView, 
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView,
    enroll_course,
    CourseListAPIView, 
    CourseDetailAPIView,
    submit_feedback,
    ModuleCreateView,
    ModuleUpdateView,
    ModuleDeleteView,
    delete_notification,
    delete_module_notification,
    remove_student,
    get_user_likes,
    toggle_like
)

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    
    # Put specific patterns BEFORE generic slug patterns
    path('new/', CourseCreateView.as_view(), name='course_create'),
    path('api/courses/', CourseListAPIView.as_view(), name='api_course_list'),
    
    # Module URLs (put before course detail to avoid conflicts)
    path('<slug:course_slug>/module/add/', ModuleCreateView.as_view(), name='module_create'), 
    path('module/<int:pk>/update/', ModuleUpdateView.as_view(), name='module_update'), 
    path('module/<int:pk>/delete/', ModuleDeleteView.as_view(), name='module_delete'),
    path('<slug:course_slug>/remove_student/<int:student_id>/', remove_student, name='remove_student'),
    
    # Enrollment and feedback URLs
    path('<int:pk>/enroll/', enroll_course, name='enroll_course'),
    path('<int:course_id>/feedback/', submit_feedback, name='submit_feedback'),
    
    # delete notification URLs
    path('notification/delete/<int:notification_id>/', delete_notification, name='delete_notification'),
    path('notification/module/delete/<int:notification_id>/', delete_module_notification, name='delete_module_notification'),
    
    # API detail URL
    path('api/courses/<slug:slug>/', CourseDetailAPIView.as_view(), name='api_course_detail'),
    
    # Course CRUD URLs - put these AFTER more specific patterns
    path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('<slug:slug>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<slug:slug>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    # Add to urls.py
    path('api/courses/<int:course_id>/like/', toggle_like, name='api_toggle_like'),
    path('api/user/likes/', get_user_likes, name='api_user_likes'),
]