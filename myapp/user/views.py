from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from .forms import RegisterForm, LoginForm

# Create your views here.

### Registration
class Registration(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, 'user/user_register.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = RegisterForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('blog:list')

### Login
class Login(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = LoginForm()

        context = {
            'form': form,
        }
        return render(request, 'user/user_login.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = LoginForm(request.POST)
        # print(form)
        print(form.errors)
        # if form.is_valid():
        # email = form.cleaned_data['email']
        email = form.data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=email, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect('blog:list')
        
        form.add_error(None, '아이디가 없습니다.')
        context = {
            'form': form,
        }
        return render(request, 'user/user_login.html', context)

# class Login(View):
#     def get(self, request):
#         ### 추가한 내용
#         if request.user.is_authenticated:
#             return redirect('blog:list')
        
#         form = LoginForm()
#         context = {
#             'form': form
#         }
#         return render(request, 'user/user_login.html', context)
        
#     def post(self, request):
#         ### 추가한 내용
#         if request.user.is_authenticated:
#             return redirect('blog:list')
        
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(username=email, password=password) # True, False
            
#             if user:
#                 login(request, user)
#                 return redirect('blog:list')
            
#             form.add_error(None, '아이디가 없습니다.')
        
#         context = {
#             'form': form
#         }
        
#         return render(request, 'user/user_login.html', context)


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('blog:list')
