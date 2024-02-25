from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

import uuid

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
    # isPrivate: Resume can only be seen in groups the user is in.
    # Later, it should be possible for the user to select which resumes the private group should see, but we can implement that later.
    isPrivate = models.BooleanField(default=True)
    # isHidden: No one except resume owner can see it
    isHidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name

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

# We will use this class to eventually implement promotion feature if owner is deleted
class UserPrivateGroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(PrivateGroup, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')

class JoinRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(PrivateGroup, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=2000, blank=True)

# Stores messages posted in private group homepages
class PrivateGroupBoardComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(PrivateGroup, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=2000, blank=False)

