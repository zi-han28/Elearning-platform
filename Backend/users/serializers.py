from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Profile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "is_teacher"]
        extra_kwargs = {"email": {"required": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    class Meta:
        model = Profile
        fields = ["username", "email", "profile_picture", "status", "bio"]

    def update(self, instance, validated_data):
        new_pic = validated_data.get("profile_picture")
        if new_pic and instance.profile_picture.name != "profile_pics/default.jpg":
            instance.profile_picture.delete(save=False)
        return super().update(instance, validated_data)

class PublicUserSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="profile.status", read_only=True)
    profile_picture = serializers.ImageField(source="profile.profile_picture", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "is_teacher", "is_student", "status", "profile_picture"]
        