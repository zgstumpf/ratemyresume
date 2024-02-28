from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

import uuid

class PrivateGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Ideally, if owner is deleted, there should be staff that can be promoted, but this can be implemented later.
    owner = models.ForeignKey(User, related_name='owner_privateGroup', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)
    members = models.ManyToManyField(User, related_name='user_privateGroup', through='UserPrivateGroupMembership')
    # If allowJoinRequests is true, users can see the group in search.
    allowJoinRequests = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# We will use this class to eventually implement promotion feature if owner is deleted
class UserPrivateGroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(PrivateGroup, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')

# This is how users request to join a group if they haven't been invited
class JoinRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(PrivateGroup, on_delete=models.CASCADE)

    actionChoices = models.TextChoices('actionChoices', 'accepted rejected')
    action = models.CharField(choices=actionChoices, max_length=8, null=True)

    action_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

# This is how owners invite users to join a group
class GroupInvite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # sender is basically same thing as owner
    sender = models.ForeignKey(User, related_name='sender_user', on_delete=models.CASCADE)
    group = models.ForeignKey(PrivateGroup, on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, related_name='invitee_user', on_delete=models.CASCADE)

    # I followed Django docs, but feel like there must be a  a better way to do this
    actionChoices = models.TextChoices('actionChoices', 'accepted rejected')
    action = models.CharField(choices=actionChoices, max_length=8, null=True)

    action_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

# Stores messages posted in private group homepages
class PrivateGroupBoardComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(PrivateGroup, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=2000, blank=False)

class Resume(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True)
    file = models.FileField(upload_to='resumes/files/')
    description = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ratingsEnabled = models.BooleanField(default=True)
    commentsEnabled = models.BooleanField(default=True)

    visibilityChoices = models.TextChoices('visibilityChoices', 'public visible_to_my_groups shared_with_specific_groups hidden')
    visibility = models.CharField(choices=visibilityChoices, max_length=27)

    groupsSharedWith = models.ManyToManyField(PrivateGroup, through='ResumeGroupViewingPermissions')

    def __str__(self):
        return self.name

class ResumeGroupViewingPermissions(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    group = models.ForeignKey(PrivateGroup, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('resume', 'group')

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # The same user can't leave multiple ratings on one resume
        unique_together = ['user', 'resume']

    def __str__(self):
        return self.value



