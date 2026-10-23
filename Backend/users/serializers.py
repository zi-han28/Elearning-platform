from attr import fields
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password2", "is_teacher"]
        extra_kwargs = {"email": {"required": True}, "password": {"write_only": True}, "password2": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data.pop("password2"):
            return serializers.ValidationError({"password2":"Passwords do not match"})
        return data
    
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


class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["is_teacher"] = user.is_teacher
        return token