from rest_framework import permissions


class IsTeacher(permissions.BasePermission):
    # only teachers can create courses
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_teacher)


class IsCourseTeacherOrReadOnly(permissions.BasePermission):
    # anyone can read, only the teacher who owns the course (or the module's course) can edit
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        course = getattr(obj, "course", obj)
        return request.user == course.teacher
