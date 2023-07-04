from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import Post, Comment, HashTag
# from django.contrib.auth import get_user_model
from .forms import PostForm, CommentForm, HashTagForm


class Index(View):
    def get(self, request):
        posts = Post.objects.all()
        context = {
            "posts": posts
        }
        return render(request, 'blog/post_list.html', context)


# class List(ListView):
#     # get_queryset()
#     # paginate_by # 페이지를 끊어주는 것
#     # template_name = 'blog/board.html' # 템플릿 이름을 지정하고싶을 때. 기본값이 있음.
#     model = Post
#     context_object_name = 'posts' # 전달해주는 context의 이름


class Write(LoginRequiredMixin, View):

    def get(self, request):
        form = PostForm()
        context = {
            "form": form,
        }
        return render(request, 'blog/post_form.html', context)

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            user = request.user
            post.writer = user
            post.save()
            return redirect('blog:list')
        form.add_error(None, '폼이 유효하지 않습니다.')
        context = {
            'form': form,
        }
        return render(request, 'blog/post_form.html', context)


class DetailView(View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post=post)
        hashTags = HashTag.objects.filter(post=post)
        commentForm = CommentForm
        hashTagForm = HashTagForm
        context = {
            "post": post,
            "comments": comments,
            "hashTags": hashTags,
            "commentForm": commentForm,
            "hashTagForm": hashTagForm,
        }
        return render(request, 'blog/post_detail.html', context)


# class Update(UpdateView):
#     model = Post
#     # form_class = PostForm
#     template_name = 'blog/post_edit.html'
#     fields = ['title', 'content']

#     def get_success_url(self): # get_absolute_url
#         post = self.get_object()
#         return reverse('blog:detail', kwargs={'post_id': post.pk})
    
#     # def get_absolute_url(self):
#     # success_url = reverse_lazy(f"blog:detail", kwargs={'pk': self.object.pk})

#     def get_initial(self): # 없어도 딱히 됨. 조작할게아니라면
#         initial = super().get_initial()
#         post = self.get_object()
#         initial['title'] = post.title
#         initial['content'] = post.content
#         return initial


class Update(View):

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        form = PostForm(initial={'title': post.title, 'content': post.content})
        context = {
            "form": form,
            "post": post,
        }
        return render(request, 'blog/post_edit.html', context)

    def post(self, request, post_id):
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(pk=post_id)
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            return redirect("blog:detail", post_id=post_id)
        form.add_error(None, '폼이 유효하지 않습니다.')
        context = {
            'form': form,
        }
        return render(request, 'blog/post_edit.html', context)


# class Delete(DeleteView):
#     model = Post
#     success_url = reverse_lazy("blog:list")

#     def post(self, request, *args, **kwargs):
#         self.get_object().delete()
#         return redirect(self.success_url)


class Delete(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.delete()
        return redirect('blog:list')


### Comment
class CommentWrite(View):
    
    def post(self, request, post_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            print(user)
            content = form.cleaned_data['content']
            post = Post.objects.get(pk=post_id)
            comment = Comment.objects.create(post=post, content=content, writer=user)
            return redirect('blog:detail', post_id=post.pk)
        form.add_error(None, '폼이 유효하지 않습니다.')
        context = {
            'form': form,
        }
        return render(request, 'blog/form_error.html', context)



class CommentDelete(View):

    def post(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        post_id = comment.post.pk
        # post_id = comment.post.id # pk도 되고 id도 되네요.
        comment.delete()
        return redirect('blog:detail', post_id=post_id)


### HashTag
class HashTagWrite(View):

    def post(self, request, post_id):
        form = HashTagForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            post = Post.objects.get(pk=post_id)
            hashTag = HashTag.objects.create(name=name, post=post, writer=user)
            return redirect('blog:detail', post_id=post_id)
        form.add_error(None, '폼이 유효하지 않습니다.')
        context = {
            'form': form,
        }
        return render(request, 'blog/form_error.html', context)


class HashTagDelete(View):

    def post(self, request, hashTag_id):
        hashTag = HashTag.objects.get(pk=hashTag_id)
        post_id = hashTag.post.id
        hashTag.delete()
        return redirect('blog:detail', post_id=post_id)