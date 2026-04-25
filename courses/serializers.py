from rest_framework import serializers
from .models import Course, Module

# module serializer
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'file', 'file_type']

# course serializer
class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    teacher = serializers.StringRelatedField()
    
    class Meta:
        model = Course
        fields = [
            'id', 
            'title', 
            'slug', 
            'teacher', 
            'overview', 
            'course_picture', 
            'created', 
            'modules'
        ]