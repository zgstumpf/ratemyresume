from django.forms import ModelForm
from resumes.models import Resume, Comment, Rating

class UploadResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'description', 'file']
        labels = {
            'name': 'Give this resume a name',
            'description': 'Give this resume a description. What areas are you unsure about, what parts do you want others to focus on?',
            'file': 'Upload resume (pdf required)',
        }

class UploadCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Make a comment'
        }

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        labels = {
            'value': 'Rating'
        }
