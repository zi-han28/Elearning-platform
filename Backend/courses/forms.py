from django import forms
from .models import Course, Module, Feedback

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'overview', 'course_picture']
        widgets = {
            'overview': forms.Textarea(attrs={'rows': 4}),
        }

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'order', 'file', 'file_type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'order': forms.NumberInput(attrs={'min': 1}),
            'file' :forms.FileInput(attrs={'accept': '.pdf,.docx,.pptx,.txt,.mp4,.jpg,.png'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].help_text = 'Upload images or pdfs.'

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your feedback about this course:'}),
        }