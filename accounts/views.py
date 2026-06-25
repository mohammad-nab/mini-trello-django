from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home:home")

        return render(
            request,
            "accounts/login.html",
            {"form": form}
        )


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("home:home")
