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
    toggle_like,
    enroll_course_api,
    remove_student_api,
    feedback_api,
    ModuleListCreateAPIView,
    ModuleDetailAPIView,
    notifications_api,
    EnrollmentNotificationDeleteAPIView,
    ModuleNotificationDeleteAPIView,
)

urlpatterns = [
    # ---- JWT API endpoints ----
    path('api/courses/', CourseListAPIView.as_view(), name='api_course_list'),
    path('api/courses/<int:pk>/enroll/', enroll_course_api, name='api_enroll_course'),
    path('api/courses/<int:course_id>/feedback/', feedback_api, name='api_feedback'),
    path('api/courses/<int:course_id>/like/', toggle_like, name='api_toggle_like'),
    path('api/courses/<slug:course_slug>/modules/', ModuleListCreateAPIView.as_view(), name='api_module_list'),
    path('api/courses/<slug:course_slug>/students/<int:student_id>/', remove_student_api, name='api_remove_student'),
    path('api/courses/<slug:slug>/', CourseDetailAPIView.as_view(), name='api_course_detail'),
    path('api/modules/<int:pk>/', ModuleDetailAPIView.as_view(), name='api_module_detail'),
    path('api/notifications/', notifications_api, name='api_notifications'),
    path('api/notifications/enrollment/<int:pk>/', EnrollmentNotificationDeleteAPIView.as_view(), name='api_delete_notification'),
    path('api/notifications/module/<int:pk>/', ModuleNotificationDeleteAPIView.as_view(), name='api_delete_module_notification'),
    path('api/user/likes/', get_user_likes, name='api_user_likes'),

    # ---- template views ----
    path('', CourseListView.as_view(), name='course_list'),
    
    # Put specific patterns BEFORE generic slug patterns
    path('new/', CourseCreateView.as_view(), name='course_create'),
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
    
    # Course CRUD URLs - put these AFTER more specific patterns
    path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('<slug:slug>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<slug:slug>/delete/', CourseDeleteView.as_view(), name='course_delete'),
]