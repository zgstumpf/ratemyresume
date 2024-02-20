from django.shortcuts import render
from django.core import serializers
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
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
    comment_form = UploadCommentForm()
    rating_form = RatingForm()

    print(request.POST)
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.POST['form_type'] == 'comment_form':
            comment_form = UploadCommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user_id = request.user.id
                comment.resume_id = resume_id
                comment.save()

                return JsonResponse({"comment": comment.text}, status=200)
        elif request.POST['form_type'] == 'rating_form':
            print("rating form")
            rating_form = RatingForm(request.POST)

            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.user_id = request.user.id
                rating.resume_id = resume_id
                rating.save()

                return JsonResponse({"rating": rating.value}, status=200)

    try:
        resume = Resume.objects.get(pk=resume_id)
    except Resume.DoesNotExist:
        raise Http404("Resume does not exist")

    pdf_path = resume.file.path

    with open(pdf_path, 'rb') as pdf_file:
        pdf_content = base64.b64encode(pdf_file.read()).decode()

    # '-' before field name makes order_by do descending
    comments = Comment.objects.filter(resume_id=resume_id).order_by('-created_at')
    ratings = Rating.objects.filter(resume_id=resume_id).order_by('-created_at')

    return render(request, "resumes/details.html", {"resume": resume, "pdf": pdf_content, "comment_form": comment_form, "rating_form": rating_form, "comments": comments, "ratings": ratings})

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