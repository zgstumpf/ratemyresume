from django.forms import ModelForm
from resumes.models import Resume, Comment, Rating

class UploadResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['file', 'name', 'description']
        labels = {
            'file': 'Upload resume (pdf required)',
            'name': 'If you had to refer to this specific resume, what name would you use?',
            'description': "Discussion prompt: The message you put here will be displayed at the top of this resume's comment section.",
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
