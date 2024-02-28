from django import forms
from django.forms import ModelForm
from resumes.models import Resume, Comment, Rating, PrivateGroup, GroupInvite, UserPrivateGroupMembership

class UploadResumeForm(ModelForm):
    groupsSharedWith = forms.ModelMultipleChoiceField(queryset=None)
    class Meta:
        model = Resume
        fields = ['file', 'name', 'description', 'visibility', 'groupsSharedWith']
        labels = {
            'file': 'Upload resume (pdf required)',
            'name': 'If you had to refer to this specific resume, what name would you use?',
            'description': "Discussion prompt: The message you put here will be displayed at the top of this resume's comment section.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Your custom query here to populate groupsSharedWith
        self.fields['groupsSharedWith'].queryset = PrivateGroup.objects.all()
        self.fields['groupsSharedWith'].label_from_instance = lambda obj: obj.__str__()

    for group in PrivateGroup.objects.all():
        print(group.__str__())

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

class CreatePrivateGroupForm(ModelForm):
    class Meta:
        model = PrivateGroup
        fields = ['name', 'description', 'allowJoinRequests']

class GroupInviteForm(ModelForm):
    class Meta:
        model = GroupInvite
        fields = ['invitee']
