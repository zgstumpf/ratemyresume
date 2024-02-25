from django.shortcuts import render
from django.core import serializers
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from pdf2image import convert_from_path

import json
import base64
from io import BytesIO

from .models import Resume, Comment, Rating
from .forms import UploadResumeForm, UploadCommentForm, RatingForm

# View for homepage
def index(request):
    resumes = Resume.objects.order_by("created_at")

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

    try:
        resume = Resume.objects.get(pk=resume_id)
    except Resume.DoesNotExist:
        raise Http404("Resume does not exist")

    pdf_path = resume.file.path
    with open(pdf_path, 'rb') as pdf_file:
        pdf_content = base64.b64encode(pdf_file.read()).decode()

    # '-' before field name makes order_by do descending
    comments = Comment.objects.filter(resume_id=resume_id).order_by('-created_at')

    avgRating = None
    userRating = None

    # Get all ratings for the specific resume, and find the average value
    ratings = Rating.objects.filter(resume_id=resume_id)
    if ratings:
        ratingsValues = [rating.value for rating in ratings]
        avgRating = round(sum(ratingsValues) / len(ratingsValues),2)
        # Out of those ratings, find the one that belongs to the signed in user
        userRating = ratings.filter(user_id=request.user.id).get()

    context = {
        "resume": resume,
        "pdf": pdf_content,
        "comment_form": comment_form,
        "rating_form": rating_form,
        "comments": comments,
        # Only return the avg rating - If we returned all the ratings, anyone could see who gave what rating.
        "avgRating": avgRating,
        # Return user's rating so they can see what and when they rated the resume in the past
        "userRating": userRating
    }

    return render(request, "resumes/details.html", context)

def view_pdf(request, resume_id):
    resume = Resume.objects.get(pk=resume_id)
    with open(resume.file.path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + resume.file.name
    return response

@login_required
def upload(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = UploadResumeForm(request.POST, request.FILES)

        # Check if the form is valid and call cleaning functions:
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user_id = request.user.id
            resume.save()


            # redirect to a new URL:
            return HttpResponseRedirect(f'/details/{resume.id}/')

    # If this is a GET (or any other method) create the default form.
    else:
        form = UploadResumeForm()

    return render(request, 'resumes/upload.html', {'form': form})

def user(request, user_id):
    user = User.objects.get(pk=user_id)
    username = user.username
    resumes = Resume.objects.filter(user_id=user_id).order_by('-created_at')
    attachAvgAndNumRatings(resumes)
    attachImagesAsStrings(resumes)

    context = {
        'resumes': resumes,
        'isUserHome': user_id == request.user.id, #True if user searched for themself
        'thisPageUsername': username
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