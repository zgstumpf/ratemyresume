from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
    HttpResponseForbidden,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count, OuterRef, Subquery, Avg
from django.template.loader import render_to_string
from django.utils import timezone
from pdf2image import convert_from_path
from django.conf import settings

import base64
from io import BytesIO
from datetime import timedelta
import subprocess
import os

from .models import (
    Resume,
    Comment,
    Rating,
    PrivateGroup,
    GroupInvite,
    JoinRequest,
    ResumeGroupViewingPermissions,
    UserPrivateGroupMembership,
)
from .forms import (
    UploadResumeForm,
    EditResumeForm,
    UploadCommentForm,
    RatingForm,
    CreatePrivateGroupForm,
)


# View for homepage
def index(request):
    new_resumes = Resume.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=72)
    )
    new_resumes = [
        r for r in new_resumes if isUserPermittedToViewResume(request.user, r)
    ]
    new_resumes = attachAvgAndNumRatings(new_resumes)
    new_resumes = attach_has_user_rated(request.user, new_resumes)

    unrated_resumes = (
        Resume.objects.annotate(  # add field has_rating to resume
            has_rating=Subquery(
                # Get id of outer query (the resume), then find the first rating with that resume id
                # We only need the first one because we just need to check if we can even find one in the first place
                # If we can't, has_rating will be None, and we will filter it away in the next step
                Rating.objects.filter(resume_id=OuterRef("id")).values("id")[:1]
            )
        )
        .filter(
            has_rating__isnull=True
            # Unrated resumes should be separate than new ones, since most new resumes will be unrated anyway
            # Unrated resumes are the ones that have been left unrated for a while
        )
        .exclude(created_at__gte=timezone.now() - timedelta(hours=72))
    )
    unrated_resumes = [
        r for r in unrated_resumes if isUserPermittedToViewResume(request.user, r)
    ]
    unrated_resumes = attachAvgAndNumRatings(unrated_resumes)
    unrated_resumes = attach_has_user_rated(request.user, unrated_resumes)

    highest_rated_resumes = (
        Resume.objects.annotate(
            ratings=Subquery(
                Rating.objects.filter(resume_id=OuterRef("id")).values("value")
            )
        )
        .exclude(ratings__isnull=True)
        .annotate(avg_rating=Avg("ratings"))
        .order_by("-avg_rating")
    )
    highest_rated_resumes = [
        r for r in highest_rated_resumes if isUserPermittedToViewResume(request.user, r)
    ]
    # Get 30 highest rated so there is a cutoff, which will be needed if we ever do pagination
    highest_rated_resumes = highest_rated_resumes[:30]
    highest_rated_resumes = attachAvgAndNumRatings(highest_rated_resumes)
    highest_rated_resumes = attach_has_user_rated(request.user, highest_rated_resumes)

    context = {
        "new_resumes": new_resumes,
        "unrated_resumes": unrated_resumes,
        "highest_rated_resumes": highest_rated_resumes,
    }

    return render(request, "resumes/index.html", context)


def details(request, resume_id):
    # request may be sent to this view in multiple ways
    # 1. User searches URL details/<int:resume_id>/
    #    (example) request: <WSGIRequest: GET '/details/1/'>
    # 2. commentForm or ratingForm are submitted, triggering corresponding functions
    #    in details.js. These functions send AJAX POST requests to the view
    #    (example) request: <WSGIRequest: POST '/details/1/'>
    resume = get_object_or_404(Resume, pk=resume_id)

    if not isUserPermittedToViewResume(request.user, resume):
        return HttpResponseForbidden()

    # Initialize empty comment and rating forms
    comment_form = UploadCommentForm()
    rating_form = RatingForm()

    # If request originates from searching URL, request.method == 'GET'
    # If request originates from form submission, request.method == 'POST'
    if request.method == "POST":

        # 'form_type' is a hidden input field added to the comment form with a preset value of 'comment_form'
        # When the form is submitted, 'form-type' and its value will be submitted with it in the request
        # Because the details view has multiple forms, this hidden input field is used to identify the forms
        if request.POST["form_type"] == "comment_form":
            comment_form = UploadCommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)

                comment.user_id = request.user.id
                comment.resume_id = resume_id
                comment.save()

                # for AJAX
                commentHtml = render_to_string(
                    "comment.html", {"comment": comment, "resume": resume}
                ).replace("\n", "")

                return JsonResponse({"commentHtml": commentHtml}, status=200)

        elif request.POST["form_type"] == "rating_form":
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
                    defaults={"value": rating_form.cleaned_data["value"]},
                )

                return JsonResponse(
                    {"value": rating.value, "updated_at": rating.updated_at}, status=200
                )
                # After here, you enter details.js to the success block of <$('#ratingForm').submit(function (event)>

    pdf_content = pdf_to_str(resume)

    # This ratings code is copied from attachAvgAndNumRatings because passing a single object to that function
    # didn't work. TODO: Refactor.
    ratings = Rating.objects.filter(resume_id=resume.id)
    numRatings = len(ratings)
    if numRatings > 0:
        ratingsValues = [rating.value for rating in ratings]
        avgRating = round(sum(ratingsValues) / len(ratingsValues), 2)
    else:
        avgRating = None

    userRating = None
    try:
        userRating = Rating.objects.get(resume=resume_id, user=request.user.id)
    except ObjectDoesNotExist:
        userRating = None

    # '-' before field name makes order_by do descending
    comments = Comment.objects.filter(resume_id=resume_id).order_by("-created_at")
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
        "userRating": userRating,
    }

    return render(request, "resumes/details.html", context)


# TODO: ADD PERMISSION CHECKING
def view_pdf(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)

    if not isUserPermittedToViewResume(request.user, resume):
        return HttpResponseForbidden()

    with open(resume.file.path, "rb") as file:
        response = HttpResponse(file.read(), content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=" + resume.file.name

    return response


@login_required
def upload(request):
    if request.method == "POST":
        # Create a form instance and populate it with data from the request (binding):
        form = UploadResumeForm(request.POST, request.FILES, request=request)

        # Check if the form is valid and call cleaning functions:
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user_id = request.user.id
            resume.save()

            if resume.visibility == "shared_with_specific_groups":
                for group in form.cleaned_data["groupsSharedWith"]:
                    ResumeGroupViewingPermissions.objects.create(
                        resume=resume, group=group
                    )

            try:
                convert_to_pdf(resume)
            except FileNotFoundError:
                form.add_error('file', 'File failed to convert to pdf.')

            # redirect to a new URL:
            return HttpResponseRedirect(f"/details/{resume.id}/")

    # If this is a GET (or any other method) create the default form.
    else:
        form = UploadResumeForm(request=request)

    # TODO: Fix if returning an errored form, file upload is cleared.
    return render(request, "resumes/upload.html", {"form": form})


@login_required
def edit_resume(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)

    if request.user != resume.user:
        return HttpResponse("You can't edit someone else's resume.", status=403)

    if request.method == "POST":
        form = EditResumeForm(request.POST, request=request, instance=resume)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"/details/{resume.id}/")
    else:
        form = EditResumeForm(request=request, instance=resume)

    pdf_content = pdf_to_str(resume)
    return render(request, "edit_resume.html", {"form": form, "file": pdf_content})


def user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    username = user.username

    resumes = getResumesUserPermittedToView(request.user, user)
    attachAvgAndNumRatings(resumes)
    attachNumComments(resumes)

    # Initialize to prevent error when passing empty variable to context
    groupInvites = GroupInvite.objects.none()
    joinRequests = JoinRequest.objects.none()
    # If user is on someone else's page, they should see no invites.
    if request.user == user:
        groupInvites = (
            GroupInvite.objects.filter(invitee=user)
            .exclude(action__isnull=False)
            .order_by("-created_at")
        )  # later may want this in own view
        groupsUserOwns = PrivateGroup.objects.filter(owner=user).values_list(
            "id", flat=True
        )
        joinRequests = JoinRequest.objects.filter(
            group__in=groupsUserOwns, action__isnull=True
        )

    groups = PrivateGroup.objects.filter(members=user)
    for group in groups:
        group.last_activity = last_group_activity(group.id)

    context = {
        "resumes": resumes,
        "isUserHome": user_id == request.user.id,  # True if user searched for themself
        "thisPageUsername": username,
        "groupInvites": groupInvites,  # later may want this in own view
        "joinRequests": joinRequests,
        "groups": groups,
    }

    return render(request, "resumes/user.html", context)


@login_required
def delete_resume(request, resume_id):
    """
    AJAX
    """
    try:
        resume = Resume.objects.get(pk=resume_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Resume does not exist"}, status=404)

    if request.user != resume.user:
        return JsonResponse(
            {"error": "You can't delete a resume you don't own."}, status=401
        )

    # Store resume id before deleting. We need to pass id to JavaScript so the corresponding
    # resume card can be removed from the page.
    resume_id = resume.id
    resume.delete()

    return JsonResponse({"resume_id": resume_id}, status=200)


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
            avgRating = round(sum(ratingsValues) / len(ratingsValues), 1)
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
        image = convert_from_path(path)[0]  # 0 means do first page only
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        resume.imageData = f"data:image/jpeg;base64,{img_str}"
    return resumes


def get_resume_preview_image(request, resume_id):
    try:
        resume = Resume.objects.get(pk=resume_id)

        if not isUserPermittedToViewResume(request.user, resume):
            return JsonResponse(
                {"error": f"Unauthorized to view preview for resume {resume_id}"},
                status=401,
            )

        path = resume.file.path
        # Convert PDFs to image
        image = convert_from_path(path)[0]  # 0 means do first page only
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        imageData = f"data:image/jpeg;base64,{img_str}"
        return JsonResponse({"image": imageData}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({"error": f"Resume {resume_id} does not exist"}, status=404)
    except:
        return JsonResponse(
            {
                "error": f"Unexpected error occured while getting preview image for resume {resume_id}"
            },
            status=500,
        )


def attachNumComments(resumes):
    for resume in resumes:
        comments = Comment.objects.filter(resume_id=resume.id)
        numComments = len(comments)
        resume.numComments = numComments
    return resumes


def attach_has_user_rated(user, resumes):
    """
    Adds property hasUserRated to each resume
    """
    for resume in resumes:
        userRating = Rating.objects.filter(resume_id=resume.id, user_id=user.id)
        resume.hasUserRated = True if userRating else False
    return resumes


def creategroup(request):
    createPrivateGroupForm = CreatePrivateGroupForm()
    if request.method == "POST":
        createPrivateGroupForm = CreatePrivateGroupForm(request.POST)
        if createPrivateGroupForm.is_valid():
            # createPrivateGroupForm.owner_id = request.user.id
            # idk what members looks like - members in form needs to be multiselect anyway
            cleaned_data = createPrivateGroupForm.cleaned_data
            name = cleaned_data.get("name")
            description = cleaned_data.get("description")
            allowJoinRequests = cleaned_data.get("allowJoinRequests")
            # Set the owner of the group
            owner = request.user
            # Create the PrivateGroup instance and save it
            newGroup = PrivateGroup.objects.create(
                owner=owner,
                name=name,
                description=description,
                allowJoinRequests=allowJoinRequests,
            )

            # Owners are also technically members - This is helpful when determining mutual groups between users
            UserPrivateGroupMembership.objects.create(user=owner, group=newGroup)

            return HttpResponseRedirect(
                f"/group/{newGroup.id}/"
            )  # should redirect to new page
    return render(
        request,
        "resumes/creategroup.html",
        {"createPrivateGroupForm": createPrivateGroupForm},
    )


def grouppage(request, group_id):
    group = get_object_or_404(PrivateGroup, pk=group_id)
    requestingUserIsOwner = group.owner == request.user
    requestingUserIsMember = request.user in group.members.all()
    if requestingUserIsOwner:
        joinRequests = JoinRequest.objects.filter(group=group)
        groupInvites = GroupInvite.objects.filter(group=group)
    elif requestingUserIsMember:
        joinRequests = JoinRequest.objects.filter(group=group, user=request.user)
        groupInvites = GroupInvite.objects.filter(group=group, invitee=request.user)
    else:
        joinRequests = JoinRequest.objects.none()
        groupInvites = GroupInvite.objects.none()

    joinRequestsPending = joinRequests.filter(action__isnull=True)
    joinRequestsHistory = joinRequests.filter(action__isnull=False)
    groupInvitesPending = groupInvites.exclude(action__isnull=False)
    groupInvitesHistory = groupInvites.exclude(action__isnull=True)

    # call getResumesUserPermittedToView for all members of group, where each group member is parameter resume owner
    # first priority: resumes that have been specifically shared with the group
    # second priority: resumes "shared with my groups"
    # third: public resumes and resumes for signed in users
    resumes = Resume.objects.none()
    for member in group.members.all():
        member_resumes = getResumesUserPermittedToView(request.user, member)
        member_resumes = (
            member_resumes.order_by()
        )  # remove ordering since calling union on ordered queryset produces error
        resumes = resumes.union(member_resumes)
        resumes = attach_has_user_rated(request.user, resumes)
        attachAvgAndNumRatings(resumes)

    context = {
        "group": group,
        "isOwner": requestingUserIsOwner,
        "isMember": requestingUserIsMember,
        "joinRequests": joinRequests,
        "joinRequestsPending": joinRequestsPending,
        "joinRequestsHistory": joinRequestsHistory,
        "groupInvitesPending": groupInvitesPending,
        "groupInvitesHistory": groupInvitesHistory,
        "resumes": resumes,
    }

    return render(request, "resumes/grouppage.html", context)


def groups(request):
    groups = PrivateGroup.objects.all()

    for group in groups:
        group.last_activity = last_group_activity(group.id)

    return render(request, "resumes/groups.html", {"groups": groups})


def sendinvite(request):
    """
    AJAX
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    invitee_id = request.POST.get("invitee_id")
    group_id = request.POST.get("group_id")

    try:
        group = PrivateGroup.objects.get(pk=group_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Group does not exist"}, status=404)

    try:
        invitee = User.objects.get(pk=invitee_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Invitee does not exist"}, status=404)

    if invitee in group.members.all():
        return JsonResponse(
            {"error": "Invitee is already a member of the group"}, status=500
        )

    if (
        GroupInvite.objects.filter(group=group, invitee=invitee)
        .exclude(action__isnull=False)
        .exists()
    ):
        return JsonResponse(
            {"error": "Invitee already has a pending invite to this group"}, status=500
        )

    GroupInvite.objects.create(
        invitee=invitee, sender=request.user, group=group  # group owner
    )

    return JsonResponse({"message": "Invitation sent"}, status=200)


def acceptinvite(request, invite_id):
    """
    AJAX
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    try:
        invite = GroupInvite.objects.get(pk=invite_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Does not exist"}, status=404)

    if request.user != invite.invitee:
        return JsonResponse(
            {"error": "You are not the invitee of this invitation."}, status=401
        )

    invite.group.members.add(invite.invitee)
    invite.action = "accepted"
    invite.action_at = timezone.now()
    invite.save()

    groupCardHtml = render_to_string(
        "group_card.html", {"group": invite.group}
    ).replace("\n", "")

    return JsonResponse(
        {"group": invite.group.name, "groupCardHtml": groupCardHtml}, status=200
    )


def rejectinvite(request, invite_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    try:
        invite = GroupInvite.objects.get(pk=invite_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Does not exist"}, status=404)

    if request.user != invite.invitee:
        return JsonResponse(
            {"error": "You are not the invitee of this invitation."}, status=401
        )

    invite.action = "rejected"
    invite.action_at = timezone.now()
    invite.save()

    return JsonResponse({"group": invite.group.name}, status=200)


def sendrequest(request, group_id):
    """
    Uses AJAX. Activated when user clicks 'Request to join' button on a group page.
    """
    if request.method != "POST":
        return HttpResponse("Method Not Allowed", status=405)
    if request.user.is_authenticated == False:
        return JsonResponse({"error": "You are not logged in"}, status=401)

    # Why not just skip this line and plug group_id=group_id into the create()?
    # - Because doing that, Django would not validate that group_id links to an existing group.
    try:
        group = PrivateGroup.objects.get(pk=group_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Does not exist"}, status=404)

    # Members of a group can not request to join the group
    if request.user in group.members.all():
        return JsonResponse(
            {"error": "You are already a member of this group"}, status=400
        )

    # Find the user's join requests for the group. Remove join requests that have been acted upon.
    # If any are left, it means the user already has pending join request.
    if (
        JoinRequest.objects.filter(group=group, user=request.user)
        .exclude(action__isnull=False)
        .exists()
    ):
        return JsonResponse(
            {"error": "You already have a pending join request."}, status=400
        )

    JoinRequest.objects.create(
        user=request.user,
        group=group,
    )
    return JsonResponse({"message": "sent request"}, status=200)


def acceptrequest(request, joinRequest_id):
    try:
        joinRequest = JoinRequest.objects.get(pk=joinRequest_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Does not exist"}, status=404)

    group = joinRequest.group

    # Do not confuse request with joinRequest here!
    # Only owner can accept request
    if group.owner != request.user:
        return JsonResponse({"error": "unauthorized"}, status=401)

    group.members.add(joinRequest.user)
    joinRequest.action = "accepted"
    joinRequest.action_at = timezone.now()
    joinRequest.save()
    return JsonResponse(
        {
            "message": "Accepted",
            "group": group.name,
            "newMember": joinRequest.user.username,
        },
        status=200,
    )  # ajax


def rejectrequest(request, joinRequest_id):
    try:
        joinRequest = JoinRequest.objects.get(pk=joinRequest_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Does not exist"}, status=404)

    group = joinRequest.group

    # Do not confuse request with joinRequest here!
    if group.owner != request.user:
        return JsonResponse({"error": "unauthorized"}, status=401)

    joinRequest.action = "rejected"
    joinRequest.action_at = timezone.now()
    joinRequest.save()
    return JsonResponse(
        {"message": "Join request successfully rejected"}, status=200
    )  # ajax


def getResumesUserPermittedToView(requestingUser: User, resumeOwner: User):
    """
    Returns all resumes, most recent first, from resumeOwner that requestingUser is permitted to view
    """
    resumeOwnerResumes = Resume.objects.filter(user=resumeOwner)
    if requestingUser == resumeOwner:
        return resumeOwnerResumes.order_by("-created_at")
    else:
        resumesForUser = Resume.objects.none()

        publicResumes = resumeOwnerResumes.filter(visibility="public")
        if publicResumes.exists():
            resumesForUser = resumesForUser.union(publicResumes)

        if not requestingUser.is_authenticated:
            return resumesForUser.order_by("-created_at")

        resumesForSignedInUsers = resumeOwnerResumes.filter(
            visibility="signed_in_users"
        )
        if resumesForSignedInUsers.exists():
            resumesForUser = resumesForUser.union(resumesForSignedInUsers)

        mutualGroupResumes = Resume.objects.none()
        if hasMutualGroups(requestingUser, resumeOwner):
            mutualGroupResumes = resumeOwnerResumes.filter(
                visibility="visible_to_my_groups"
            )
        if mutualGroupResumes.exists():
            resumesForUser = resumesForUser.union(mutualGroupResumes)

        specificGroupResumes = resumeOwnerResumes.filter(
            visibility="shared_with_specific_groups",
            id__in=getPermittedSpecificGroupResumeIds(requestingUser),
        )
        if specificGroupResumes.exists():
            resumesForUser = resumesForUser.union(specificGroupResumes)

        return resumesForUser.order_by("-created_at")


def isUserPermittedToViewResume(user: User, resume: Resume):
    """
    Returns True if user is permitted to view resume, False otherwise.

    Make sure user and resume exist before calling this function.
    """
    if resume.visibility == "public":
        return True

    # If the resume owner is logged in, they can see their own resume.
    if user == resume.user:
        return True

    if resume.visibility == "signed_in_users" and user.is_authenticated():
        return True
    # No need to check if user is authenticated past here - if the user is not authenticated, the user object passed
    # to the following functions will cause the function to return false

    if resume.visibility == "visible_to_my_groups" and hasMutualGroups(
        user, resume.user
    ):
        return True

    if (
        resume.visibility == "shared_with_specific_groups"
        and resume.id in getPermittedSpecificGroupResumeIds(user)
    ):
        return True

    # Only other visibility setting is 'hidden'
    return False


def hasMutualGroups(user1: User, user2: User):
    if not isinstance(user1, User) or not isinstance(user2, User):
        return False

    return (
        UserPrivateGroupMembership.objects.filter(user__in=[user1, user2])
        .values("group_id")
        .annotate(num_users=Count("user_id", distinct=True))
        .filter(num_users=2)
        .exists()
    )


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
    userGroupIds = UserPrivateGroupMembership.objects.filter(user=user).values_list(
        "group_id", flat=True
    )
    # Look through the ResumeGroupViewingPermissions table. Retrieve resume_id if that resume is associated with a group_id from above list.
    # The ResumeGroupViewingPermissions table only stores resume_ids of resumes that have visibility set to 'shared_with_specific_groups'
    permittedResumeIds = ResumeGroupViewingPermissions.objects.filter(
        group_id__in=userGroupIds
    ).values_list("resume_id", flat=True)
    # TODO: should I return an empty of class type(permittedResumeIds) instead of ResumeGroupViewingPermissions class if user is anonymous?
    return permittedResumeIds


def resumeSearch(request):
    query = request.GET.get("query", "")

    resumes = Resume.objects.filter(
        Q(name__contains=query) | Q(description__contains=query)
    )

    # Search results can't show resumes the user isn't allowed to see
    resumes = [r for r in resumes if isUserPermittedToViewResume(request.user, r)]

    resumes = attach_has_user_rated(request.user, resumes)
    resumes = attachAvgAndNumRatings(resumes)

    # % include 'resume_card.html' with resume_id=resume.id user_id=resume.user.id user=resume.user resume_name=resume.name hasUserRated=resume.hasUserRated created_at=resume.created_at avgRating=resume.avgRating numRatings=resume.numRatings%
    resume_html_list = []
    for resume in resumes:
        resume_html = render_to_string(
            "resume_card.html",
            {
                "resume_id": resume.id,
                "user_id": resume.user.id,
                "user": resume.user,
                "requestingUser": request.user,
                "resume_name": resume.name,
                "hasUserRated": resume.hasUserRated,
                "created_at": resume.created_at,
                "avgRating": resume.avgRating,
                "numRatings": resume.numRatings,
            },
        ).replace("\n", "")
        resume_html_list.append(resume_html)

    return JsonResponse({"results": resume_html_list}, status=200)


def group_search(request):
    query = request.GET.get("query", "")

    groups = PrivateGroup.objects.filter(
        Q(name__contains=query) | Q(description__contains=query)
    )

    for group in groups:
        group.last_activity = last_group_activity(group.id)

    groups_html_list = []
    for group in groups:
        group_html = render_to_string("group_card.html", {"group": group}).replace(
            "\n", ""
        )
        groups_html_list.append(group_html)

    return JsonResponse({"results": groups_html_list}, status=200)


def user_search(request):
    """
    AJAX. Returns HTML invite forms for users that can be invited to a certain group.
    """
    query = request.GET.get("query", "")
    group_id = request.GET.get("group_id", "")

    try:
        group = PrivateGroup.objects.get(pk=group_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            {"error": "Something went wrong - This page does not have a group id."},
            status=404,
        )

    group_member_ids = group.members.all().values_list("id", flat=True)
    pending_invite_ids = GroupInvite.objects.filter(group=group_id).values_list(
        "invitee_id", flat=True
    )
    excluded_ids = group_member_ids.union(pending_invite_ids)

    users = User.objects.filter(
        Q(username__contains=query)
        | Q(email__contains=query)
        | Q(first_name__contains=query)
        | Q(last_name__contains=query)
    ).exclude(
        id__in=excluded_ids
    )  # Do not return users who are already in the group

    users_html_list = []
    for user in users:
        user_html = render_to_string(
            "invite_user_select.html", {"user": user, "group_id": group_id}
        ).replace("\n", "")
        users_html_list.append(user_html)

    return JsonResponse({"results": users_html_list}, status=200)


def last_group_activity(group_id: str):
    """
    Returns `datetime.datetime` object that is the more recent of:
    - the last time a member joined the group
    - the last time a resume was specifically shared with the group
    """
    # return time when last member joined, or when resume was specifically shared with group
    lastMemberJoinDate = (
        UserPrivateGroupMembership.objects.filter(group_id=group_id)
        .order_by("-join_date")
        .values_list("join_date", flat=True)
        .first()
    )

    resumeIdsSharedSpecificallyWithGroup = ResumeGroupViewingPermissions.objects.filter(
        group_id=group_id
    ).values_list("resume_id", flat=True)
    lastSpecificResumeShareDate = (
        Resume.objects.filter(id__in=resumeIdsSharedSpecificallyWithGroup)
        .order_by("-created_at")
        .values_list("created_at", flat=True)
        .first()
    )

    # If a resume was never specifically shared with the group, lastSpecificResumeShareDate will be None, and max will break.
    # In this case, remove it before evaluating max.
    # lastMemberJoinDate will never be None since the owner is made a member upon creating the group.
    return max(filter(None, [lastMemberJoinDate, lastSpecificResumeShareDate]))


def pdf_to_str(resume: Resume) -> str:
    """
    Returns a string representing the contents of a resume's file. This string can be inserted into an HTML template with:
    ```html
    <embed src="data:application/pdf;base64,{{ pdf_string }}" type="application/pdf" width="..." height="...">
    ```
    """
    with open(resume.file.path, "rb") as file:
        return base64.b64encode(file.read()).decode()


def convert_to_pdf(resume: Resume) -> str:
    """
    Uses LibreOffice to convert a resume's file to pdf in media storage. LibreOffice must be installed on the device.
    """
    output_dir = os.path.join(settings.MEDIA_ROOT, "resumes")
    original_full_filepath = os.path.join(settings.MEDIA_ROOT, resume.file.name)

    # Convert file to pdf, store in same directory
    subprocess.run(
        f'/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf --outdir {output_dir} "{resume.file.path}"',
        shell=True,
    )

    # When converting, LibreOffice keeps the filename the same but changes extension to .pdf
    original_filename = os.path.basename(resume.file.path)
    pdf_filename = os.path.splitext(original_filename)[0] + ".pdf"
    pdf_full_filepath = os.path.join(output_dir, pdf_filename)

    if os.path.exists(pdf_full_filepath):
        # LibreOffice conversion succeeded

        # In database, point resume to new pdf file
        resume.file.name = f"resumes/{pdf_filename}"
        resume.save()

        # Now that pdf file is created, delete original file
        os.remove(original_full_filepath)

        return pdf_full_filepath
    else:
        # LibreOffice conversion failed
        raise FileNotFoundError
