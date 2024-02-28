from django import forms
from django.forms import ModelForm
from resumes.models import Resume, Comment, Rating, PrivateGroup, GroupInvite, UserPrivateGroupMembership

class UploadResumeForm(ModelForm):
    groupsSharedWith = forms.ModelMultipleChoiceField(queryset=None, required=False)
    class Meta:
        model = Resume
        fields = ['file', 'name', 'description', 'visibility']
        labels = {
            'file': 'Upload resume (pdf required)',
            'name': 'If you had to refer to this specific resume, what name would you use?',
            'description': "Discussion prompt: The message you put here will be displayed at the top of this resume's comment section.",
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(UploadResumeForm, self).__init__(*args, **kwargs)

        self.fields['groupsSharedWith'].queryset = UserPrivateGroupMembership.objects.filter(user=request.user).values_list('group', flat=True)

        # Hide groupsSharedWith field by default
        #self.fields['groupsSharedWith'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        visibility = cleaned_data.get("visibility")
        groups_shared_with = cleaned_data.get("groupsSharedWith")
        # Validate that groupsSharedWith is selected only if visibility is set to 'shared_with_specific_groups'
        if visibility == 'shared_with_specific_groups' and not groups_shared_with:
            raise forms.ValidationError("Please select at least one group.")
        return cleaned_data

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
