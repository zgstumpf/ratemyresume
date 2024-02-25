from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import JsonResponse

from .forms import SignUpForm

# Can not be named just 'logout'
def logout_page(request):
    logout(request)
    return render(request, "resumes/index.html")


def login_page(request):
    authenticationForm = AuthenticationForm()
    if request.method == 'POST':
        authenticationForm = AuthenticationForm(request, data=request.POST)
        if authenticationForm.is_valid():
            username = authenticationForm.cleaned_data['username']
            password = authenticationForm.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(f'/user/{user.id}/')

    return render(request, 'login.html', {"authenticationForm": authenticationForm})

def signup(request):
    signUpForm = SignUpForm()
    if request.method == 'POST':
        signUpForm = SignUpForm(request.POST)
        if signUpForm.is_valid():
            username = signUpForm.cleaned_data['username']
            password = signUpForm.cleaned_data['password']

            user = User.objects.create_user(username=username, password=password)

            user = authenticate(request, username=username, password=password)
            login(request, user)
            # If POST was made with AJAX, we would use return JsonResponse({'success': True, "redirectURL": f'/user/{user.id}/'}, status=200)
            return redirect(f'/user/{user.id}/')

    return render(request, 'signup.html', {"signUpForm": signUpForm})