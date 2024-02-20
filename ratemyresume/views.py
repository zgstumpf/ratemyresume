from django.shortcuts import render
from django.contrib.auth import logout

# Can not be named just 'logout'
def logout_page(request):
    logout(request)
    return render(request, "resumes/index.html")