from django.forms import ModelForm
from django.contrib.auth.models import User

class SignUpForm(ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']