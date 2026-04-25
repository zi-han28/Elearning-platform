# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# custom user
class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if self.is_teacher:
            self.is_student = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

# profile model
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        default='profile_pics/default.jpg',
        upload_to='profile_pics/'
    )
    bio = models.TextField(max_length=500, blank=True)

    Status_option = [
        ('active', 'Active'),
        ('not_active', 'Not Active'),
        ('busy', 'Busy'),
        ('anonymous', 'Anonymous'),
    ]

    status = models.CharField(max_length=20, choices=Status_option, default ='active')

    def __str__(self):
        return f'{self.user.username} Profile'

# Signal to create a profile when a user is created
@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to save the profile when the user is saved
@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()