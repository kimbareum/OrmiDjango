from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PostSerializer, CommentSerializer, HashTagSerializer

from .models import Post, Comment, HashTag
# from django.contrib.auth import get_user_model

class Index(APIView):
    
    def get(self, request):
        posts = Post.objects.all()
        serialized_posts = PostSerializer(posts, many=True)
        return Response(serialized_posts.data)


class Write(LoginRequiredMixin, APIView):

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(commit=False)
            user = request.user
            post.writer = user
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailView(APIView):
    
    def get(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        comments = Comment.objects.filter(post=post)
        serialized_comments = CommentSerializer(comments, many=True)
        hashTags = HashTag.objects.filter(post=post)
        serialized_hashTags = HashTagSerializer(hashTags, many=True)
        serialized_post = PostSerializer(post)
        context = {
            "post": serialized_post.data, 
            "comments": serialized_comments.data,
            "hashTags": serialized_hashTags.data
            }
        return Response(context)


class Update(APIView):

    def get(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        serialized_post = PostSerializer(post)
        return Response(serialized_post.data)

    def post(self, request, post_id):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Delete(APIView):

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        post.delete()
        context = {
            "post_id": post_id,
        }
        return Response(context, status=status.HTTP_202_ACCEPTED)


### Comment
class CommentWrite(LoginRequiredMixin, APIView):
    
    def post(self, request, post_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                post = Post.objects.get(pk=post_id)
            except ObjectDoesNotExist as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            user = request.user
            content = serializer.data.get('content')
            try:
                comment = Comment.objects.create(post=post, content=content, writer=user)
            except ObjectDoesNotExist as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            context = {
                "post_id": post_id,
            }
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class CommentDelete(APIView):

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        post_id = comment.post.pk
        comment.delete()
        context = {
            "post_id": post_id,
        }
        return Response(context, status=status.HTTP_202_ACCEPTED)


# ### HashTag
# class HashTagWrite(LoginRequiredMixin, View):

#     def post(self, request, post_id):
#         form = HashTagForm(request.POST)
#         post = Post.objects.get(pk=post_id)
#         if form.is_valid():
#             user = request.user
#             name = form.cleaned_data['name']
#             hashTag = HashTag.objects.create(name=name, post=post, writer=user)
#             return redirect('blog:detail', post_id=post_id)
#         commentForm = CommentForm()
#         context = {
#             'post': post,
#             'comments': post.comment_set.all(),
#             'hashTags': post.hashtag_set.all(),
#             'commentForm': commentForm,
#             'hashTagForm': form,
#             'title': 'Blog',
#         }
#         return render(request, 'blog/post_detail.html', context)


# class HashTagDelete(View):

#     def post(self, request, hashTag_id):
#         hashTag = HashTag.objects.get(pk=hashTag_id)
#         post_id = hashTag.post.id
#         hashTag.delete()
#         return redirect('blog:detail', post_id=post_id)