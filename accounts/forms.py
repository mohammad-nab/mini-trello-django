from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserLoginForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()