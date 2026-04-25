# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserSearchForm
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import CustomUser

# register funciton
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('course_list')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# profile functioin
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'u_form': u_form, 'p_form': p_form})

# user search function
@login_required
def user_search(request):
    form = UserSearchForm(request.GET or None)
    users = CustomUser.objects.none()
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        user_type = form.cleaned_data.get('user_type', 'all')
        
        # Base queryset
        users = CustomUser.objects.exclude(id=request.user.id)
        
        # Filter by user type
        if user_type == 'teachers':
            users = users.filter(is_teacher=True)
        elif user_type == 'students':
            users = users.filter(is_student=True)
        
        # Apply search query if provided
        if search_query:
            users = users.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(profile__status__icontains=search_query)
            ).distinct()
    
    return render(request, 'users/user_search.html', {
        'form': form,
        'users': users,
        'search_performed': 'search_query' in request.GET
    })

# profile view
@login_required
def profile_view(request, user_id):
    
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'users/user_profile.html', {
        'viewed_user': user
    })