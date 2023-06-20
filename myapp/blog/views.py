from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

# Create your views here.
# def index(request):
#     if request.method == 'GET':
#         return HttpResponse('Index page GET')
#     return HttpResponse('Unvalid Access')


class Index(View):
    def get(self, request):
        return render(request, 'blog/board.html')
        # return HttpResponse('Index page GET class')
