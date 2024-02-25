from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import JsonResponse

from .forms import SignUpForm

# Can not be named just 'logout'
def logout_page(request):
    logout(request)
    return render(request, "resumes/index.html")


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(f'/user/{user.id}/')  # Redirect to home page after successful login

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            # Add user to database
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            return JsonResponse({"error": "Username is taken"}, status=400)

        user = authenticate(request, username=username, password=password)
        login(request, user)
        # Because this POST request is made with AJAX, we can't call redirect() here
        return JsonResponse({'success': True, "redirectURL": f'/user/{user.id}/'}, status=200)

    return render(request, 'signup.html')