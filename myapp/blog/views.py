from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm


# class Index(View):
#     def get(self, request):
#         post_objs = Post.objects.all()
#         context = {
#             "posts": post_objs,
#             # "posts": None,
#         }
#         return render(request, 'blog/board.html', context)
#         # return HttpResponse('Index page GET class')


# # write
# def write(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save()
#             return redirect('blog:list')
#     form = PostForm()
#     return render(request, 'blog/write.html', {'form': form})


class List(ListView):
    # get_queryset()
    # paginate_by # 페이지를 끊어주는 것
    # template_name = 'blog/board.html' # 템플릿 이름을 지정하고싶을 때. 기본값이 있음.
    model = Post
    context_object_name = 'posts' # 전달해주는 context의 이름


class Write(CreateView):
    model = Post
    form_class = PostForm # form_class, form_valid()
    success_url = reverse_lazy('blog:list')


class Detail(DetailView):
    model = Post
    # template_name = 'blog/post_detail.html'
    context_object_name = 'post'
