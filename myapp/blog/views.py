from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Post, Comment
from .forms import PostForm, CommentForm


### Post
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


# class Detail(DetailView):
#     model = Post
#     # template_name = 'blog/post_detail.html'
#     context_object_name = 'post'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         context['comments'] = Comment.objects.filter(post=post)
#         return context


class DetailView(View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post=post)
        context = {
            "post": post,
            "comments": comments,
        }
        return render(request, 'blog/post_detail.html', context)


class Update(UpdateView):
    model = Post
    # form_class = PostForm
    template_name = 'blog/post_edit.html'
    fields = ['title', 'content']

    def get_success_url(self): # get_absolute_url
        post = self.get_object()
        return reverse('blog:detail', kwargs={'pk': post.pk})
    
    # def get_absolute_url(self):
    # success_url = reverse_lazy(f"blog:detail", kwargs={'pk': self.object.pk})

    # def get_initial(self):
    #     initial = super().get_initial()
    #     post = self.get_object()
    #     initial['title'] = post.title
    #     initial['content'] = post.content
    #     return initial


class Delete(DeleteView):
    model = Post
    success_url = reverse_lazy("blog:list")

    def post(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect(self.success_url)


### Comment
class CommentWrite(View):
    
    def post(self, request, post_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            post = Post.objects.get(pk=post_id)
            comment = Comment.objects.create(post=post, content=content)
            return redirect('blog:detail', pk=post.pk)