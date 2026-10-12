# users/forms.py
from pickle import FALSE
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

#  user register form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    is_teacher = forms.BooleanField(
        required=False,
        label='Register as instructor',
        help_text='Check this if you want to create courses'
    )

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2', 
            'is_teacher'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = self.cleaned_data['is_teacher']
        if commit:
            user.save()
        return user

# user udpate
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

# profile udpate
class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}))
    status = forms.ChoiceField(
        choices= Profile.Status_option,
        required= FALSE,
        widget= forms.Select(attrs={'class':'form-control'})
    )
    
    class Meta:
        model = Profile
        fields = ['profile_picture','status', 'bio']
    
    def save(self, commit=True):
            profile = super().save(commit=False)
            if self.cleaned_data['profile_picture']:
                # Delete old profile picture if it's not the default
                if profile.profile_picture and profile.profile_picture.name != 'profile_pics/default.jpg':
                    profile.profile_picture.delete(save=False)
                profile.profile_picture = self.cleaned_data['profile_picture']
            if commit:
                profile.save()
            return profile

# user search  
class UserSearchForm(forms.Form):
    search_query = forms.CharField(
        label='Search Users',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by username, email, or status',
            'class': 'form-control'
        })
    )
    user_type = forms.ChoiceField(
        choices=[
            ('all', 'All Users'),
            ('teachers', 'Teachers Only'),
            ('students', 'Students Only')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )