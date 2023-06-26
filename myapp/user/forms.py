from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(forms.ModelForm):

    # password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

        widgets = {
            'password': forms.PasswordInput()
        }


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']

        widgets = {
            'password': forms.PasswordInput()
        }