from django.utils.text import slugify
from rest_framework import serializers
from users.serializers import PublicUserSerializer
from .models import Course, Module, Enrollment, Feedback, EnrollmentNotification, ModuleNotification, Like

# module serializer
class ModuleSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(slug_field="slug", read_only=True)

    class Meta:
        model = Module
        fields = ["id", "course", "title", "description", "order", "file", "file_type"]

    def validate_order(self, value):
        if value < 1:
            raise serializers.ValidationError("Order must be at least 1.")
        return value

# feedback serializer
class FeedbackSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source="student.username", read_only=True)

    class Meta:
        model = Feedback
        fields = ["id", "course", "student", "comment", "commented_at"]
        read_only_fields = ["course", "commented_at"]

# course list serializer (lightweight)
class CourseListSerializer(serializers.ModelSerializer):
    teacher = serializers.CharField(source="teacher.username", read_only=True)
    like_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "slug", "teacher", "overview", "course_picture", "created", "like_count"]

# course detail / create / update serializer
class CourseSerializer(serializers.ModelSerializer):
    teacher = PublicUserSerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    feedbacks = FeedbackSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source="likes.count", read_only=True)
    enrolled = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    user_feedback_exists = serializers.SerializerMethodField()
    enrolled_students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "slug",
            "teacher",
            "overview",
            "course_picture",
            "created",
            "modules",
            "feedbacks",
            "like_count",
            "enrolled",
            "liked",
            "user_feedback_exists",
            "enrolled_students",
        ]
        read_only_fields = ["slug", "created"]

    def _user(self):
        request = self.context.get("request")
        return request.user if request and request.user.is_authenticated else None

    def get_enrolled(self, obj):
        user = self._user()
        return bool(user) and Enrollment.objects.filter(student=user, course=obj).exists()

    def get_liked(self, obj):
        user = self._user()
        return bool(user) and Like.objects.filter(student=user, course=obj).exists()

    def get_user_feedback_exists(self, obj):
        user = self._user()
        return bool(user) and Feedback.objects.filter(student=user, course=obj).exists()

    # only the course teacher can see the list of enrolled students
    def get_enrolled_students(self, obj):
        user = self._user()
        if user != obj.teacher:
            return None
        return PublicUserSerializer(obj.students.all().order_by("username"), many=True, context=self.context).data

    def create(self, validated_data):
        validated_data["slug"] = slugify(validated_data["title"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        new_pic = validated_data.get("course_picture")
        if new_pic and instance.course_picture and instance.course_picture.name != "course_pics/default.jpg":
            instance.course_picture.delete(save=False)
        return super().update(instance, validated_data)

    def validate_title(self, value):
        # slug is generated from the title on create only
        if not self.instance and Course.objects.filter(slug=slugify(value)).exists():
            raise serializers.ValidationError("A course with this title already exists.")
        return value

# notification serializers
class EnrollmentNotificationSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    student = serializers.CharField(source="student.username", read_only=True)

    class Meta:
        model = EnrollmentNotification
        fields = ["id", "course", "student", "message", "created_at"]

class ModuleNotificationSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    module = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ModuleNotification
        fields = ["id", "course", "module", "message", "created_at"]
