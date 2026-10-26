# Workspace Structure

Files listed in .gitignore will be excluded.

## Configuration Files

### requirements.txt
```
altair==5.5.0
amqp==5.3.1
asgiref==3.9.1
attrs==25.3.0
autobahn==24.4.2
Automat==25.4.16
billiard==4.2.1
blinker==1.9.0
boto3==1.40.17
botocore==1.40.17
cachetools==6.1.0
celery==5.5.3
certifi==2025.8.3
cffi==1.17.1
channels==4.3.1
channels_redis==4.3.0
charset-normalizer==3.4.3
click==8.2.1
click-didyoumean==0.3.1
click-plugins==1.1.1.2
click-repl==0.3.0
constantly==23.10.4
crispy-bootstrap5==2025.6
cryptography==45.0.6
daphne==4.2.1
Django==5.2.5
django-allauth==65.10.0
django-crispy-forms==2.4
django-storages==1.14.6
djangorestframework==3.16.1
gitdb==4.0.12
GitPython==3.1.45
gunicorn==23.0.0
hyperlink==21.0.0
idna==3.10
incremental==24.7.2
Jinja2==3.1.6
jmespath==1.0.1
jsonschema==4.25.1
jsonschema-specifications==2025.4.1
kombu==5.5.4
MarkupSafe==3.0.2
msgpack==1.1.1
narwhals==2.1.2
numpy==2.3.2
packaging==25.0
pandas==2.3.1
pillow==11.3.0
prompt_toolkit==3.0.51
protobuf==6.32.0
pyarrow==21.0.0
pyasn1==0.6.1
pyasn1_modules==0.4.2
pycparser==2.22
pydeck==0.9.1
pyOpenSSL==25.1.0
python-dateutil==2.9.0.post0
pytz==2025.2
redis==6.4.0
referencing==0.36.2
requests==2.32.5
rpds-py==0.27.0
s3transfer==0.13.1
service-identity==24.2.0
six==1.17.0
smmap==5.0.2
sqlparse==0.5.3
streamlit==1.48.1
tenacity==9.1.2
toml==0.10.2
tornado==6.5.2
Twisted==25.5.0
txaio==25.6.1
typing_extensions==4.14.1
tzdata==2025.2
urllib3==2.5.0
vine==5.1.0
wcwidth==0.2.13
whitenoise==6.9.0
zope.interface==7.2
django-cors-headers
djangorestframework-simplejwt
PyJWT
psycopg2-binary
python-dotenv
```

## File Structure

- 📁 Backend/
  - 📁 Backend/
    - 📄 __init__.py
    - 📄 asgi.py
      - Imports:
        - import os
        - import django.core.asgi.get_asgi_application
        - import channels.routing.ProtocolTypeRouter
        - import channels.routing.URLRouter
        - import channels.auth.AuthMiddlewareStack
        - import channels.security.websocket.AllowedHostsOriginValidator
        - import chat.routing
    - 📄 celery.py
      - Imports:
        - import os
        - import celery.Celery
    - 📄 settings.py
      - Imports:
        - import os
        - import pathlib.Path
        - import datetime.timedelta
        - import dotenv.load_dotenv
        - import os
        - import dj_database_url
    - 📄 urls.py
      - Imports:
        - import django.contrib.admin
        - import django.shortcuts.redirect
        - import django.urls.path
        - import django.urls.include
        - import django.conf.settings
        - import django.conf.urls.static.static
        - import users.views as user_views
        - import users.views.CreateUserView
        - import users.views.CustomTokenView
        - import rest_framework_simplejwt.views.TokenRefreshView
    - 📄 wsgi.py
      - Imports:
        - import os
        - import django.core.wsgi.get_wsgi_application
  - 📁 chat/
    - 📄 __init__.py
    - 📄 admin.py
    - 📄 apps.py
      - Imports:
        - import django.apps.AppConfig
      - Classes:
        - ChatConfig
    - 📄 consumers.py
      - Imports:
        - import json
        - import channels.generic.websocket.AsyncWebsocketConsumer
        - import django.contrib.auth.models.AnonymousUser
        - import .models.ChatMessage
        - import django.utils.timezone
        - import courses.models.Course
      - Classes:
        - ChatConsumer
    - 📁 migrations/
      - 📄 0001_initial.py
        - Imports:
          - import django.db.migrations
          - import django.db.models
        - Classes:
          - Migration
      - 📄 0002_initial.py
        - Imports:
          - import django.db.models.deletion
          - import django.db.migrations
          - import django.db.models
        - Classes:
          - Migration
      - 📄 0003_initial.py
        - Imports:
          - import django.db.models.deletion
          - import django.conf.settings
          - import django.db.migrations
          - import django.db.models
        - Classes:
          - Migration
      - 📄 __init__.py
    - 📄 models.py
      - Imports:
        - import django.db.models
        - import django.db.models
        - import courses.models.Course
        - import users.models.CustomUser
      - Classes:
        - ChatMessage
      - Methods:
        - __str__
    - 📄 routing.py
      - Imports:
        - import django.urls.re_path
        - import ..consumers
    - 📁 templates/
      - 📁 chat/
        - 📄 room.html
    - 📄 tests.py
      - Imports:
        - import django.test.TestCase
        - import django.test.Client
        - import django.urls.reverse
        - import django.contrib.auth.get_user_model
        - import courses.models.Course
        - import .models.ChatMessage
        - import django.utils.timezone
      - Classes:
        - ChatAppTests
      - Methods:
        - setUp
        - test_chat_room_view_authenticated
        - test_chat_message_creation
        - test_chat_message_ordering
        - test_chat_message_str_representation
        - test_chat_room_context_data
    - 📄 urls.py
      - Imports:
        - import django.urls.path
        - import ..views
    - 📄 views.py
      - Imports:
        - import django.shortcuts.render
        - import django.shortcuts.get_object_or_404
        - import courses.models.Course
        - import django.contrib.auth.decorators.login_required
        - import .models.ChatMessage
      - Functions:
        - chat_room
  - 📁 courses/
    - 📄 __init__.py
    - 📄 admin.py
      - Imports:
        - import django.contrib.admin
    - 📄 apps.py
      - Imports:
        - import django.apps.AppConfig
      - Classes:
        - CoursesConfig
    - 📄 forms.py
      - Imports:
        - import django.forms
        - import .models.Course
        - import .models.Module
        - import .models.Feedback
      - Classes:
        - CourseForm
        - ModuleForm
        - FeedbackForm
      - Methods:
        - __init__
    - 📁 migrations/
      - 📄 0001_initial.py
        - Imports:
          - import django.db.migrations
          - import django.db.models
        - Classes:
          - Migration
      - 📄 0002_initial.py
        - Imports:
          - import django.db.models.deletion
          - import django.conf.settings
          - import django.db.migrations
          - import django.db.models
        - Classes:
          - Migration
      - 📄 __init__.py
    - 📄 models.py
      - Imports:
        - import email.message
        - import django.db.models
        - import django.urls.reverse
        - import users.models.CustomUser
      - Classes:
        - Course
        - Module
        - Enrollment
        - EnrollmentNotification
        - Feedback
        - ModuleNotification
        - Like
      - Methods:
        - get_course_picture_url
        - __str__
        - get_absolute_url
    - 📄 permissions.py
      - Imports:
        - import rest_framework.permissions
      - Classes:
        - IsTeacher
        - IsCourseTeacherOrReadOnly
      - Methods:
        - has_permission
        - has_object_permission
    - 📄 routing.py
      - Imports:
        - import django.urls.re_path
        - import ..consumers
    - 📄 serializers.py
      - Imports:
        - import django.utils.text.slugify
        - import rest_framework.serializers
        - import users.serializers.PublicUserSerializer
        - import .models.Course
        - import .models.Module
        - import .models.Enrollment
        - import .models.Feedback
        - import .models.EnrollmentNotification
        - import .models.ModuleNotification
        - import .models.Like
      - Classes:
        - ModuleSerializer
        - FeedbackSerializer
        - CourseListSerializer
        - CourseSerializer
        - EnrollmentNotificationSerializer
        - ModuleNotificationSerializer
      - Methods:
        - validate_order
        - _user
        - get_enrolled
        - get_liked
        - get_user_feedback_exists
        - get_enrolled_students
        - create
        - update
        - validate_title
    - 📄 tasks.py
    - 📄 tests.py
      - Imports:
        - import django.test.TestCase
        - import django.test.Client
        - import django.urls.reverse
        - import django.contrib.auth.get_user_model
        - import django.core.files.uploadedfile.SimpleUploadedFile
        - import django.utils.text.slugify
        - import django.core.exceptions.ValidationError
        - import .models.Course
        - import .models.Module
        - import .models.Enrollment
        - import .models.Feedback
        - import .models.EnrollmentNotification
        - import .models.ModuleNotification
        - import .forms.CourseForm
        - import .forms.ModuleForm
        - import .forms.FeedbackForm
        - import users.models.CustomUser
      - Classes:
        - CourseModelTests
        - ModuleModelTests
        - EnrollmentModelTests
        - NotificationModelTests
        - CourseFormTests
        - ModuleFormTests
        - FeedbackFormTests
        - CourseViewTests
        - ModuleViewTests
        - NotificationViewTests
      - Methods:
        - setUp
        - test_course_creation
        - test_course_str_representation
        - test_course_get_absolute_url
        - test_course_get_course_picture_url
        - test_module_creation
        - test_module_str_representation
        - test_module_ordering
        - test_enrollment_creation
        - test_enrollment_unique_together
        - test_enrollment_str_representation
        - test_enrollment_notification_creation
        - test_module_notification_creation
        - test_valid_course_form
        - test_invalid_course_form
        - test_valid_module_form
        - test_invalid_module_form
        - test_valid_feedback_form
        - test_course_list_view
        - test_course_detail_view
        - test_course_create_view_authenticated_teacher
        - test_course_create_view_authenticated_student
        - test_enroll_course_authenticated
        - test_module_create_view_authenticated_teacher
        - test_module_create_view_authenticated_student
        - test_delete_enrollment_notification_authenticated_teacher
    - 📄 urls.py
      - Imports:
        - import django.urls.path
        - import .views.(
    - 📄 views.py
      - Imports:
        - import django.shortcuts.render
        - import django.shortcuts.get_object_or_404
        - import django.shortcuts.redirect
        - import django.views.generic.ListView
        - import django.views.generic.DetailView
        - import django.views.generic.CreateView
        - import django.views.generic.UpdateView
        - import django.views.generic.DeleteView
        - import django.contrib.auth.mixins.LoginRequiredMixin
        - import django.contrib.auth.mixins.UserPassesTestMixin
        - import django.urls.reverse_lazy
        - import django.urls.reverse
        - import .models.Course
        - import .models.Module
        - import .models.Enrollment
        - import .models.Feedback
        - import .models.EnrollmentNotification
        - import .models.ModuleNotification
        - import .models.Like
        - import .forms.CourseForm
        - import .forms.ModuleForm
        - import .forms.FeedbackForm
        - import django.contrib.messages
        - import rest_framework.generics
        - import rest_framework.permissions
        - import .serializers.(
        - import .permissions.IsTeacher
        - import .permissions.IsCourseTeacherOrReadOnly
        - import rest_framework.status
        - import rest_framework.exceptions.PermissionDenied
        - import rest_framework.parsers.MultiPartParser
        - import rest_framework.parsers.FormParser
        - import rest_framework.parsers.JSONParser
        - import django.utils.text.slugify
        - import django.http.HttpResponseForbidden
        - import django.http.JsonResponse
        - import django.contrib.auth.decorators.login_required
        - import users.models.CustomUser
        - import rest_framework.decorators.api_view
        - import rest_framework.decorators.permission_classes
        - import rest_framework.response.Response
        - import django.views.decorators.csrf.csrf_exempt
        - import django.views.decorators.http.require_http_methods
      - Functions:
        - get_user_likes
        - toggle_like
        - enroll_course
        - delete_notification
        - remove_student
        - submit_feedback
        - delete_module_notification
        - enroll_course_api
        - remove_student_api
        - feedback_api
        - notifications_api
      - Classes:
        - CourseListView
        - CourseDetailView
        - CourseCreateView
        - CourseUpdateView
        - CourseDeleteView
        - ModuleCreateView
        - ModuleUpdateView
        - ModuleDeleteView
        - CourseListAPIView
        - CourseDetailAPIView
        - ModuleListCreateAPIView
        - ModuleDetailAPIView
        - EnrollmentNotificationDeleteAPIView
        - ModuleNotificationDeleteAPIView
      - Methods:
        - get_context_data
        - form_valid
        - test_func
        - get_course
        - get_success_url
        - get_serializer_class
        - get_permissions
        - perform_create
        - get_queryset
  - 📄 manage.py
    - Imports:
      - import os
      - import sys
    - Functions:
      - main
  - 📁 media/
    - 📁 course_pics/
    - 📁 module_files/
    - 📁 profile_pics/
  - 📁 static/
    - 📁 css/
    - 📁 js/
      - 📄 main.js
  - 📁 template/
    - 📄 base.html
    - 📁 courses/
      - 📄 course_delete.html
      - 📄 course_detail.html
      - 📄 course_feedback.html
      - 📄 course_form.html
      - 📄 course_list.html
      - 📄 course_material.html
      - 📄 module_delete.html
      - 📄 module_form.html
    - 📁 users/
      - 📄 login.html
      - 📄 logout.html
      - 📄 profile.html
      - 📄 register.html
  - 📁 users/
    - 📄 __init__.py
    - 📄 admin.py
    - 📄 api_urls.py
      - Imports:
        - import django.urls.path
        - import rest_framework_simplejwt.views.TokenRefreshView
        - import .views.(
    - 📄 apps.py
      - Imports:
        - import django.apps.AppConfig
      - Classes:
        - UsersConfig
    - 📄 forms.py
      - Imports:
        - import pickle.FALSE
        - import django.forms
        - import django.contrib.auth.forms.UserCreationForm
        - import django.contrib.auth.get_user_model
        - import .models.Profile
      - Classes:
        - UserRegisterForm
        - UserUpdateForm
        - ProfileUpdateForm
        - UserSearchForm
      - Methods:
        - save
    - 📁 migrations/
      - 📄 0001_initial.py
        - Imports:
          - import django.contrib.auth.models
          - import django.contrib.auth.validators
          - import django.db.models.deletion
          - import django.utils.timezone
          - import django.conf.settings
          - import django.db.migrations
          - import django.db.models
        - Classes:
          - Migration
      - 📄 __init__.py
    - 📄 models.py
      - Imports:
        - import django.db.models
        - import django.contrib.auth.models.AbstractUser
        - import django.db.models.signals.post_save
        - import django.dispatch.receiver
      - Functions:
        - create_profile
        - save_profile
      - Classes:
        - CustomUser
        - Profile
      - Methods:
        - save
        - __str__
    - 📄 serializers.py
      - Imports:
        - import attr.fields
        - import django.contrib.auth.get_user_model
        - import django.contrib.auth.password_validation.validate_password
        - import rest_framework.serializers
        - import .models.Profile
        - import rest_framework_simplejwt.serializers.TokenObtainPairSerializer
      - Classes:
        - UserSerializer
        - ProfileSerializer
        - PublicUserSerializer
        - CustomTokenSerializer
      - Methods:
        - validate
        - create
        - update
        - get_token
    - 📁 templates/
      - 📁 users/
        - 📄 user_profile.html
        - 📄 user_search.html
    - 📄 tests.py
      - Imports:
        - import django.test.TestCase
        - import django.test.Client
        - import django.urls.reverse
        - import django.contrib.auth.get_user_model
        - import django.core.files.uploadedfile.SimpleUploadedFile
        - import django.core.exceptions.ValidationError
        - import .models.CustomUser
        - import .models.Profile
        - import .forms.UserRegisterForm
        - import .forms.UserUpdateForm
        - import .forms.ProfileUpdateForm
        - import .forms.UserSearchForm
      - Classes:
        - CustomUserModelTests
        - ProfileModelTests
        - UserRegisterFormTests
        - UserUpdateFormTests
        - ProfileUpdateFormTests
        - UserSearchFormTests
        - UserViewTests
        - UserSearchFunctionalityTests
      - Methods:
        - setUp
        - test_create_user
        - test_create_superuser
        - test_user_str_representation
        - test_teacher_user_creation
        - test_user_save_method
        - test_profile_creation_signal
        - test_profile_str_representation
        - test_profile_status_choices
        - test_valid_registration_form
        - test_invalid_registration_form
        - test_teacher_registration
        - test_valid_user_update_form
        - test_valid_profile_update_form
        - test_valid_search_form
        - test_search_form_with_only_query
        - test_register_view_get
        - test_register_view_post_valid
        - test_profile_view_authenticated
        - test_profile_update_post
        - test_user_search_view_teacher_access
        - test_user_search_view_student_access
        - test_profile_view_by_id_authenticated
        - test_search_by_username
        - test_search_by_email
        - test_search_by_status
        - test_filter_teachers_only
        - test_filter_students_only
        - test_search_all_users
    - 📄 urls.py
      - Imports:
        - import django.urls.path
        - import ..views
    - 📄 views.py
      - Imports:
        - import django.db.migrations.serializer
        - import django.shortcuts.render
        - import django.shortcuts.redirect
        - import django.shortcuts.get_object_or_404
        - import django.contrib.auth.login
        - import django.contrib.auth.logout
        - import django.contrib.auth.get_user_model
        - import django.contrib.auth.decorators.login_required
        - import django.contrib.messages
        - import .forms.UserRegisterForm
        - import .forms.UserUpdateForm
        - import .forms.ProfileUpdateForm
        - import .forms.UserSearchForm
        - import django.http.HttpResponseForbidden
        - import django.db.models.Q
        - import .models.CustomUser
        - import .serializers.ProfileSerializer
        - import .serializers.UserSerializer
        - import .serializers.PublicUserSerializer
        - import .serializers.CustomTokenSerializer
        - import rest_framework.permissions.IsAuthenticated
        - import rest_framework.permissions.AllowAny
        - import rest_framework.generics
        - import rest_framework.parsers.MultiPartParser
        - import rest_framework.parsers.FormParser
        - import rest_framework.parsers.JSONParser
        - import rest_framework_simplejwt.views.TokenObtainPairView
      - Functions:
        - register
        - profile
        - user_search
        - profile_view
      - Classes:
        - CreateUserView
        - MyProfileView
        - UserSearchView
        - UserDetailView
        - CustomTokenView
      - Methods:
        - get_object
        - get_queryset
- 📁 Frontend/
  - 📄 README.md
  - 📄 index.html
  - 📄 package-lock.json
  - 📄 package.json
  - 📁 public/
    - 📄 favicon.svg
    - 📄 icons.svg
  - 📁 src/
    - 📄 App.jsx
      - Imports:
        - import { useState } from 'react'
        - import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
        - import Login from './pages/login'
        - import Logout from './pages/Logout'
        - import Register from './pages/register'
        - import Home from './pages/home'
        - import NotFound from './pages/NotFound'
        - import ProtectedRoute from './components/ProtectedRoute'
        - import Layout from './components/Layout'
      - Functions:
        - logout
        - RegisterAndLogout
        - App
      - Methods:
        - logout
    - 📄 api.js
      - Imports:
        - import axios from "axios"
        - import {ACCESS_TOKEN} from "./constants"
    - 📁 assets/
    - 📁 components/
      - 📄 Layout.jsx
        - Imports:
          - import { Link, Outlet, useLocation } from "react-router-dom"
          - import { Navbar, Nav, Container } from "react-bootstrap"
          - import { jwtDecode } from "jwt-decode"
          - import { ACCESS_TOKEN } from "../constants"
        - Functions:
          - Layout
      - 📄 ProtectedRoute.jsx
        - Imports:
          - import { Navigate } from "react-router-dom"
          - import { jwtDecode } from "jwt-decode"
          - import api from "../api"
          - import { REFRESH_TOKEN, ACCESS_TOKEN } from "../constants"
          - import { useEffect, useState } from "react"
        - Functions:
          - ProtectedRoute
          - refreshToken
    - 📄 constants.js
      - Exports:
        - ACCESS_TOKEN
        - REFRESH_TOKEN
    - 📄 main.jsx
      - Imports:
        - import React from 'react'
        - import ReactDOM from 'react-dom/client'
        - import { Navbar, Nav, Container } from "react-bootstrap"
        - import App from './App.jsx'
    - 📁 pages/
      - 📄 Home.jsx
        - Imports:
          - import {useState, useEffect} from "react"
          - import api from "../api"
        - Functions:
          - Home
      - 📄 Login.jsx
        - Imports:
          - import { useState } from "react"
          - import { Link, useNavigate } from "react-router-dom"
          - import api from "../api"
          - import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants"
        - Functions:
          - Login
          - handleSubmit
      - 📄 Logout.jsx
        - Functions:
          - Logout
      - 📄 NotFound.jsx
        - Functions:
          - NotFound
      - 📄 Profile.jsx
        - Imports:
          - import {useState, useEffect} from "react"
          - import { data, Link, useNavigate } from "react-router-dom"
          - import api from "../api"
        - Functions:
          - Profile
          - handleChange
          - msg
      - 📄 Register.jsx
        - Imports:
          - import { useState } from "react"
          - import { Link, useNavigate } from "react-router-dom"
          - import api from "../api"
        - Functions:
          - Field
          - Register
          - handleChange
          - handleSubmit
    - 📁 styles/
      - 📄 style.css
  - 📄 vite.config.js
    - Imports:
      - import react from '@vitejs/plugin-react'
      - import { defineConfig } from 'vite'
- 📄 project-structure.md
- 📄 requirements.txt
