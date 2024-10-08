from django import forms
from django.forms import ModelForm
from resumes.models import Resume, Comment, Rating, PrivateGroup, GroupInvite

class UploadResumeForm(ModelForm):
    # For some reason, if you initialize groupsSharedWith to CheckboxSelectMultiple, it doesn't work,
    # but changing it to CheckboxSelectMultiple through the __init__method works.
    groupsSharedWith = forms.ModelMultipleChoiceField(queryset=None, label='Share with the following groups:', required=False)
    class Meta:
        model = Resume
        fields = ['file', 'name', 'description', 'commentsEnabled', 'visibility', 'groupsSharedWith']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['value'] = f"{request.user}'s resume"
        self.fields['name'].widget.attrs['class'] = 'min-width-80'

        self.fields['description'].widget = forms.Textarea(attrs={'class': 'min-width-80', 'rows': 2})

       # User can only select groups they are a member of
        self.fields['groupsSharedWith'].widget = forms.CheckboxSelectMultiple()
        self.fields['groupsSharedWith'].queryset = PrivateGroup.objects.filter(members=request.user)
        # Sets label of option to name of group - __str__() is defined in PrivateGroup model and is set to return name
        self.fields['groupsSharedWith'].label_from_instance = lambda group: group.__str__()

    def clean(self):
        cleaned_data = super().clean()
        visibility = cleaned_data.get('visibility')
        groupsSharedWith = cleaned_data.get('groupsSharedWith')

        if visibility == 'shared_with_specific_groups' and not groupsSharedWith:
            self.add_error('visibility', "If you chose to share with specific groups, you must select at least one group to share with.")

        return cleaned_data


class EditResumeForm(UploadResumeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta(UploadResumeForm.Meta):
        fields = ['name', 'description', 'commentsEnabled', 'visibility', 'groupsSharedWith']

    def clean(self):
        cleaned_data = super().clean()
        # Add any additional validation specific to the edit form here
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
