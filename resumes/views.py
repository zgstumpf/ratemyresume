from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.db import IntegrityError
from django.db.models import Count, QuerySet
from django.utils import timezone
from pdf2image import convert_from_path

import json
import base64
from io import BytesIO

from .models import Resume, Comment, Rating, PrivateGroup, GroupInvite, JoinRequest, ResumeGroupViewingPermissions, UserPrivateGroupMembership
from .forms import UploadResumeForm, UploadCommentForm, RatingForm, CreatePrivateGroupForm, GroupInviteForm

# View for homepage
def index(request):
    print('entered index view')
    resumes = Resume.objects.order_by("created_at")

    # TODO: may want to think about a more efficient way to do this.
    for resume in resumes:
        if not isUserPermittedToViewResume(request.user, resume):
            resumes = resumes.exclude(pk=resume.pk)

    for resume in resumes:
        path = resume.file.path
        # Convert PDFs to image
        image = convert_from_path(path)[0]
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        resume.image_data = f"data:image/jpeg;base64,{img_str}"

    return render(request, "resumes/index.html", context = {"resumes": resumes})



def details(request, resume_id):
    # request may be sent to this view in multiple ways
    # 1. User searches URL details/<int:resume_id>/
    #    (example) request: <WSGIRequest: GET '/details/1/'>
    # 2. commentForm or ratingForm are submitted, triggering corresponding functions
    #    in details.js. These functions send AJAX POST requests to the view
    #    (example) request: <WSGIRequest: POST '/details/1/'>
    # request is type: <class 'django.core.handlers.wsgi.WSGIRequest'>
    # You can use dir(request) to print all properties/methods of this class
    resume = get_object_or_404(Resume, pk=resume_id)

    if not isUserPermittedToViewResume(request.user, resume):
        return HttpResponseForbidden()

    # Initialize empty comment and rating forms
    comment_form = UploadCommentForm()
    rating_form = RatingForm()

    # If request originates from searching URL, request.method == 'GET'
    # If request originates from form submission, request.method == 'POST'
    if request.method == 'POST':
        # 'form_type' is a hidden input field added to the comment form with a preset value of 'comment_form'
        # When the form is submitted, 'form-type' and its value will be submitted with it in the request
        # Because the details view has multiple forms, this hidden input field is used to identify the forms
        if request.POST['form_type'] == 'comment_form':
            # Django takes care of extracting required info from request
            comment_form = UploadCommentForm(request.POST)

            # Django does validation and sanitizes data
            if comment_form.is_valid():
                # Save the form data to a comment object, but do not upload to database yet
                comment = comment_form.save(commit=False)

                # Add user_id (from request info) and resume_id (from URL) to comment object
                comment.user_id = request.user.id
                comment.resume_id = resume_id

                # Upload comment to database
                comment.save()

                # If we called render, every time the user makes a comment or rating, the page would refresh,
                # which would take time to load and cause a visual effect that would be annoying after a while
                # Instead, return JSON data to the JavaScript AJAX function.
                # Then, we can use JavaScript to update parts of the page without refreshing the whole page.
                comment_data = {
                    "user": request.user.username,
                    "text": comment.text,
                    "created_at": comment.created_at # TODO: date is in wrong format
                }
                return JsonResponse({"comment": comment_data}, status=200)
        elif request.POST['form_type'] == 'rating_form':
            rating_form = RatingForm(request.POST)

            if rating_form.is_valid():
                # If the user has already rated this resume before, update their rating value.
                # Else, create a new rating.
                # This logic enables users to change their rating on a resume, while still being unable
                # to rate the same resume more than once.
                # rating is the rating model that was updated or created, created is a bool that will be
                # True if the user submitted a rating for the first time
                rating, created = Rating.objects.update_or_create(
                    user_id=request.user.id,
                    resume_id=resume_id,
                    defaults={'value': rating_form.cleaned_data['value']}
                )

                return JsonResponse({"value": rating.value, "updated_at": rating.updated_at}, status=200)
                # After here, you enter details.js to the success block of <$('#ratingForm').submit(function (event)>

    pdf_path = resume.file.path
    with open(pdf_path, 'rb') as pdf_file:
        pdf_content = base64.b64encode(pdf_file.read()).decode()

    # This ratings code is copied from attachAvgAndNumRatings because passing a single object to that function
    # didn't work. TODO: Refactor.
    ratings = Rating.objects.filter(resume_id=resume.id)
    numRatings = len(ratings)
    if numRatings > 0:
        ratingsValues = [rating.value for rating in ratings]
        avgRating = round(sum(ratingsValues) / len(ratingsValues),2)
    else:
        avgRating = None


    userRating = None
    try:
        userRating = Rating.objects.get(resume=resume_id, user=request.user)
    except ObjectDoesNotExist:
        userRating = None


    # '-' before field name makes order_by do descending
    comments = Comment.objects.filter(resume_id=resume_id).order_by('-created_at')
    numComments = len(comments)

    context = {
        "resume": resume,
        "pdf": pdf_content,
        "comment_form": comment_form,
        "rating_form": rating_form,
        "comments": comments,
        "numComments": numComments,
        "avgRating": avgRating,
        "numRatings": numRatings,
        # Return user's rating so they can see what and when they rated the resume in the past
        "userRating": userRating
    }

    return render(request, "resumes/details.html", context)

# TODO: ADD PERMISSION CHECKING
def view_pdf(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)

    if not isUserPermittedToViewResume(request.user, resume):
        return HttpResponseForbidden()

    with open(resume.file.path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + resume.file.name

    return response

@login_required
def upload(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = UploadResumeForm(request.POST, request.FILES, request=request)

        # Check if the form is valid and call cleaning functions:
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user_id = request.user.id
            resume.save()

            if resume.visibility == 'shared_with_specific_groups':
                for group in form.cleaned_data['groupsSharedWith']:
                    ResumeGroupViewingPermissions.objects.create(resume=resume, group=group)

            # redirect to a new URL:
            return HttpResponseRedirect(f'/details/{resume.id}/')

    # If this is a GET (or any other method) create the default form.
    else:
        form = UploadResumeForm(request=request)

    # TODO: Fix if returning an errored form, file upload is cleared.
    return render(request, 'resumes/upload.html', {'form': form})

def user(request, user_id):
    user = User.objects.get(pk=user_id)
    username = user.username

    resumes = getResumesUserPermittedToView(request.user, user)
    attachAvgAndNumRatings(resumes)
    attachImagesAsStrings(resumes)
    attachNumComments(resumes)

    groupInvites = GroupInvite.objects.none()
    if request.user == user:
        groupInvites = GroupInvite.objects.filter(invitee=user).exclude(action__isnull=False).order_by('-created_at') # later may want this in own view

    context = {
        'resumes': resumes,
        'isUserHome': user_id == request.user.id, #True if user searched for themself
        'thisPageUsername': username,
        'groupInvites': groupInvites, # later may want this in own view
    }

    return render(request, 'resumes/user.html', context)


def attachAvgAndNumRatings(resumes):
    """
    Given a Django queryset of multiple resume objects, returns them with avgRating and numRatings properties for each.

    If there are no ratings for the resume: avgRating=None, numRatings=0
    """
    for resume in resumes:
        ratings = Rating.objects.filter(resume_id=resume.id)
        numRatings = len(ratings)
        if numRatings > 0:
            ratingsValues = [rating.value for rating in ratings]
            avgRating = round(sum(ratingsValues) / len(ratingsValues),2)
        else:
            avgRating = None
        resume.avgRating = avgRating
        resume.numRatings = numRatings
    return resumes

def attachImagesAsStrings(resumes):
    """
    SLOW - It is faster to request imageData for each image through AJAX after page has loaded.

    Given a Django queryset of multiple resume objects, returns them with imageData property for each.

    imageData is a base64 string representing the first page of the resume as a JPEG.

    Convert imageData to image in HTML: <img src="{{ resume.imageData }}">
    """
    for resume in resumes:
        path = resume.file.path
        # Convert PDFs to image
        image = convert_from_path(path)[0] # 0 means do first page only
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        resume.imageData = f"data:image/jpeg;base64,{img_str}"
    return resumes

def attachNumComments(resumes):
    for resume in resumes:
        comments = Comment.objects.filter(resume_id=resume.id)
        numComments = len(comments)
        resume.numComments = numComments
    return resumes

def creategroup(request):
    createPrivateGroupForm = CreatePrivateGroupForm()
    if request.method == 'POST':
        createPrivateGroupForm = CreatePrivateGroupForm(request.POST)
        if createPrivateGroupForm.is_valid():
            # createPrivateGroupForm.owner_id = request.user.id
            # idk what members looks like - members in form needs to be multiselect anyway
            cleaned_data = createPrivateGroupForm.cleaned_data
            name = cleaned_data.get('name')
            description = cleaned_data.get('description')
            allowJoinRequests = cleaned_data.get('allowJoinRequests')
            # Set the owner of the group
            owner = request.user
            # Create the PrivateGroup instance and save it
            newGroup = PrivateGroup.objects.create(
                owner=owner,
                name=name,
                description=description,
                allowJoinRequests=allowJoinRequests
            )

            # Owners are also technically members - This is helpful when determining mutual groups between users
            UserPrivateGroupMembership.objects.create(
                user = owner,
                group = newGroup
            )

            return HttpResponseRedirect(f'/group/{newGroup.id}/') # should redirect to new page
    return render(request, 'resumes/creategroup.html', {'createPrivateGroupForm': createPrivateGroupForm})

def grouppage(request, group_id):
    group = PrivateGroup.objects.get(pk=group_id)
    requestingUserIsOwner = group.owner == request.user
    requestingUserIsMember = request.user in group.members.all()
    if requestingUserIsOwner:
        joinRequests = JoinRequest.objects.filter(group=group)
        groupInvites = GroupInvite.objects.filter(group=group)
    else:
        joinRequests = JoinRequest.objects.filter(group=group, user=request.user)
        groupInvites = GroupInvite.objects.filter(group=group, invitee=request.user)

    joinRequestsPending = joinRequests.filter(action__isnull=True)
    joinRequestsHistory = joinRequests.filter(action__isnull=False)
    groupInvitesPending = groupInvites.exclude(action__isnull=False)
    groupInvitesHistory = groupInvites.exclude(action__isnull=True)

    context = {
        'group': group,
        'isOwner': requestingUserIsOwner,
        'isMember': requestingUserIsMember,
        'joinRequests': joinRequests,
        'joinRequestsPending': joinRequestsPending,
        'joinRequestsHistory': joinRequestsHistory,
        'groupInvitesPending': groupInvitesPending,
        'groupInvitesHistory': groupInvitesHistory
    }

    return render(request, "resumes/grouppage.html", context)

def groups(request):
    groups = PrivateGroup.objects.order_by("created_at")
    return render(request, 'resumes/groups.html', {'groups': groups})

def sendinvite(request, group_id):
    groupInviteForm = GroupInviteForm()
    if request.method == 'POST':
        groupInviteForm = GroupInviteForm(request.POST)
        if groupInviteForm.is_valid():
            cleaned_data = groupInviteForm.cleaned_data
            invitee = cleaned_data.get('invitee')
            sender = request.user
            group = PrivateGroup.objects.get(pk=group_id)

            # Can't send invites to members, can't send invites to users who have pending invites.
            if not invitee in group.members.all() and not GroupInvite.objects.filter(group=group, invitee=invitee).exclude(action__isnull=False).exists():
                GroupInvite.objects.create(
                    invitee=invitee,
                    sender=sender,
                    group=group
                )
                # Clear groupInviteForm to let user invite another user
                groupInviteForm = GroupInviteForm()
            else:
                # TODO: Later separate these error messages
                groupInviteForm.add_error('invitee', "This use is already in your group, or an invitation to this user already exists for your group.")

    return render(request, 'resumes/invite.html', {'groupInviteForm': groupInviteForm, 'group_id':group_id})

def acceptinvite(request, invite_id):
    invite = GroupInvite.objects.get(pk=invite_id)

    if request.user != invite.invitee:
        return HttpResponseForbidden("You are not permitted to perform this action.")

    invite.group.members.add(invite.invitee)
    invite.action = 'accepted'
    invite.action_at = timezone.now()
    invite.save()

    return HttpResponseRedirect(f"/group/{invite.group.id}/") #TODO: convert to ajax


def rejectinvite(request, invite_id):
    invite = GroupInvite.objects.get(pk=invite_id)

    if request.user != invite.invitee:
        return HttpResponseForbidden("You are not permitted to perform this action.")

    invite.action = 'rejected'
    invite.action_at = timezone.now()
    invite.save()

    return HttpResponseRedirect(f"/group/{invite.group.id}/") # TODO: convert to ajax


def sendrequest(request, group_id):
    # Why not just skip this line and plug group_id=group_id into the create()?
    # - Because doing that, Django would not validate that group_id links to an existing group.
    group = PrivateGroup.objects.get(pk=group_id)

    # Members of a group can not request to join the group
    # old logic: not group.members.filter(pk=request.user.id).exists():
    if not request.user in group.members.all() and not JoinRequest.objects.filter(group=group, user=request.user).exclude(action__isnull=False).exists():
        JoinRequest.objects.create(
            user=request.user,
            group=group,
        )
        return JsonResponse({"message": "sent request"}, status=200) # ajax
    return JsonResponse({"error": "You are already a member of this group, or you have a join request to this group pending."}, status=400)
    # add error handling

def acceptrequest(request, joinRequest_id):
    joinRequest = JoinRequest.objects.get(pk=joinRequest_id)
    group = joinRequest.group
    # Do not confuse request with joinRequest here!
    if request.user == group.owner:
        group.members.add(joinRequest.user)
        joinRequest.action = 'accepted'
        joinRequest.action_at = timezone.now()
        joinRequest.save()
        return JsonResponse({"message": "Accepted"}, status=200) # ajax
    else:
        return JsonResponse({"error": "unauthorized"}, status=401) # TODO: is there a better way to do this?


def rejectrequest(request, joinRequest_id):
    joinRequest = JoinRequest.objects.get(pk=joinRequest_id)
    group = joinRequest.group
    # Do not confuse request with joinRequest here!
    if request.user == group.owner:
        joinRequest.action = 'rejected'
        joinRequest.action_at = timezone.now()
        joinRequest.save()
        return JsonResponse({"message": "Join request successfully rejected"}, status=200) # ajax
    else:
        return JsonResponse({"error": "unauthorized"}, status=401) # TODO: is there a better way to do this?

def getResumesUserPermittedToView(requestingUser: User, resumeOwner: User):
    """
    Returns all resumes, most recent first, from resumeOwner that requestingUser is permitted to view
    """
    resumeOwnerResumes = Resume.objects.filter(user=resumeOwner)
    if requestingUser == resumeOwner:
        return resumeOwnerResumes.order_by('-created_at')
    else:
        resumesForUser = Resume.objects.none()

        publicResumes = resumeOwnerResumes.filter(visibility='public')
        if publicResumes.exists():
            resumesForUser = resumesForUser.union(publicResumes)

        if not requestingUser.is_authenticated:
            return resumesForUser.order_by('-created_at')

        resumesForSignedInUsers = resumeOwnerResumes.filter(visibility='signed_in_users')
        if resumesForSignedInUsers.exists():
            resumesForUser = resumesForUser.union(resumesForSignedInUsers)

        mutualGroupResumes = Resume.objects.none()
        if hasMutualGroups(requestingUser, resumeOwner):
            mutualGroupResumes = resumeOwnerResumes.filter(visibility='visible_to_my_groups')
        if mutualGroupResumes.exists():
            resumesForUser = resumesForUser.union(mutualGroupResumes)

        specificGroupResumes = resumeOwnerResumes.filter(visibility='shared_with_specific_groups',
                                                                id__in=getPermittedSpecificGroupResumeIds(requestingUser))
        if specificGroupResumes.exists():
            resumesForUser = resumesForUser.union(specificGroupResumes)

        return resumesForUser.order_by('-created_at')

def isUserPermittedToViewResume(user: User, resume: Resume):
    """
    Returns True if user is permitted to view resume, False otherwise.

    Make sure user and resume exist before calling this function.
    """
    if resume.visibility == 'public':
        return True

    # If the resume owner is logged in, they can see their own resume.
    if user == resume.user:
        return True

    if resume.visibility == 'signed_in_users' and user.is_authenticated() :
        return True

    if resume.visibility == 'visible_to_my_groups' and hasMutualGroups(user, resume.user):
        return True

    if resume.visibility == 'shared_with_specific_groups' and resume.id in getPermittedSpecificGroupResumeIds(user):
        print('resume visibility is shared with specific groups, and the user is in a group permitted by this resume.')
        return True

    # Only other visibility setting is 'hidden'
    return False


def hasMutualGroups(user1: User, user2: User):
    if not isinstance(user, User):
        return False

    return UserPrivateGroupMembership.objects.filter(user__in=[user1, user2]) \
        .values('group_id') \
        .annotate(num_users=Count('user_id', distinct=True)) \
        .filter(num_users=2) \
        .exists()

def getPermittedSpecificGroupResumeIds(user: User):
    """
    Returns Django QuerySet of UUID objects, where each UUID is a resume_id user is permitted to view because user is in a group
    the resume owner has selected to share the resume with.

    This function does not return all resume_ids user is permitted to view, just the resume_ids the resume owner has specifically
    allowed user to view due to group membership.
    """
    if not isinstance(user, User):
        return ResumeGroupViewingPermissions.objects.none()

    # Get list of group_ids of groups the user is in
    userGroupIds = UserPrivateGroupMembership.objects.filter(user=user).values_list('group_id', flat=True)
    # Look through the ResumeGroupViewingPermissions table. Retrieve resume_id if that resume is associated with a group_id from above list.
    # The ResumeGroupViewingPermissions table only stores resume_ids of resumes that have visibility set to 'shared_with_specific_groups'
    permittedResumeIds = ResumeGroupViewingPermissions.objects.filter(group_id__in=userGroupIds).values_list('resume_id', flat=True)
    print(type(permittedResumeIds)) # TODO: should I return an empty of this class instead of ResumeGroupViewingPermissions class if user is anonymous
    return permittedResumeIds