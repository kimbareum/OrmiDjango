from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProfileSerializer
from .forms import RegisterForm, LoginForm
from .models import Profile


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
        form.add_error(None, '아이디가 없습니다.')
        context = {
            'form': form,
            'title': 'User',
        }
        return render(request, 'user/user_login.html', context)


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('blog:list')


### Profile

class ProfileWrite(APIView):

    def post(self, request):
        user = request.user # request.data.get('user')
        image = request.data.get('image')
        age = request.data.get('age')
        try:
            profile = Profile.objects.create(user=user, image=image, age=age)
        except IntegrityError as e: 
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileUpdate(APIView):

    def get(self, request):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class ProfileDelete(APIView):

    def post(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        profile.delete()
        return Response("삭제 완료", status=status.HTTP_204_NO_CONTENT)