from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Can not be named just 'logout'
def logout_page(request):
    logout(request)
    return render(request, "resumes/index.html")


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/user/{}/'.format(user.id))  # Redirect to home page after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        pass
    return render(request, 'login.html')