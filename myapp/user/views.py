from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import RegisterForm, LoginForm


User = get_user_model()


# Create your views here.

### Registration
class Registration(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = RegisterForm()
        context = {
            'form': form,
            'title': 'User',
        }
        return render(request, 'user/user_register.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user:login')
        context = {
            'form': form,
            'title': 'User',
        }
        return render(request, 'user/user_register.html', context)

### Login
class Login(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = LoginForm()

        context = {
            'form': form,
            'title': 'User',
        }
        return render(request, 'user/user_login.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = LoginForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('blog:list')
        # form.add_error(None, '아이디가 없습니다.')
        context = {
            'form': form,
            'title': 'User',
        }
        return render(request, 'user/user_login.html', context)


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('blog:list')
