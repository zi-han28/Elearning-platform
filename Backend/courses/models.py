from email import message
from django.db import models
from django.urls import reverse
from users.models import CustomUser

# course model
class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=False, null=False)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses_created')
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(CustomUser, related_name='courses_joined', blank=True)
    course_picture = models.ImageField(default='course_pics/default.jpg', upload_to='course_pics/', null=True, blank=True)

    def get_course_picture_url(self):
        if self.course_picture and hasattr(self.course_picture, 'url'):
            return self.course_picture.url
        return '/media/course_pics/default.jpg'
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('course_detail', args=[self.slug])
    
# module model
class Module(models.Model):
    FILE_TYPES = (
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('document', 'document'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField()
    
    file = models.FileField(upload_to='module_files/', null=True, blank=True)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, blank=True)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.order}. {self.title}"
    
# enrollment model
class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'course')
    
    
    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
    
# enrollment notification for teachers
class EnrollmentNotification(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollment_notifications',null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment_notifications',null=True, blank=True)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollment_notices',null=True, blank=True)
    message = models.TextField(default="No students have enrolled")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Enrollment notification for {self.teacher.username} - {self.course.title}"
    

# feedback data fields
class Feedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'student')

    def __str__(self):
        return f"{self.student.username}'s feedback on {self.course.title}"
    


# module notification
class ModuleNotification(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='module_notifications')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='module_notifications')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Module notification for {self.student.username} - {self.course.title}"
    
# Like model
class Like(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='course_likes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')
        
    def __str__(self):
        return f"{self.student.username} likes {self.course.title}"