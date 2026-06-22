from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout
from . import forms


class UserRegisterView(View):
    form_class = forms.CustomUserCreationForm

    def get(self,request):
        return render(request, 'accounts/register.html', {'form':self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created for ' + user.username)
            login(request, user)
            return redirect("home:home")

        return render(
            request,
            "accounts/register.html",
            {"form": form}
        )


class UserLoginView(View):
    form_class = forms.CustomUserLoginForm
    def get(self, request):
        return render(request, 'accounts/login.html', {'form':self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home:home")

        return render(
            request,
            "accounts/login.html",
            {"form": form}
        )


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home:home")
