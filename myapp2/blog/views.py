from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, ObjectDoesNotExist
# from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PostSerializer, CommentSerializer, HashTagSerializer

from .models import Post, Comment, HashTag
# from django.contrib.auth import get_user_model

User = get_user_model()


class Index(APIView):
    
    def get(self, request):
        posts = Post.objects.all()
        serialized_posts = PostSerializer(posts, many=True)
        return Response(serialized_posts.data)


class Write(APIView):

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save(writer=request.user)
            # post = serializer.save(writer=User.objects.get(pk=1))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailView(APIView):
    
    def get(self, request, post_id):
        try:
            post = Post.objects.prefetch_related('comment_set', 'hashtag_set').get(pk=post_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        serialized_post = PostSerializer(post)
        # print(post.comment_set)
        # comments = Comment.objects.filter(post=post)
        comments = post.comment_set.all()
        serialized_comments = CommentSerializer(comments, many=True)
        # hashTags = HashTag.objects.filter(post=post)
        hashTags = post.hashtag_set.all()
        serialized_hashTags = HashTagSerializer(hashTags, many=True)
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
        post = Post.objects.get(pk=post_id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            post.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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
class CommentWrite(APIView):
    
    def post(self, request, post_id):
        # return Response(request)
        # user = request.user
        # user = User.objects.get(pk=1)
        # post = Post.objects.get(pk=post_id)11
        serializer = CommentSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            # try:
            #     post = Post.objects.get(pk=post_id)
            # except ObjectDoesNotExist as e:
            #     return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            # # user = request.user
            # user = User.objects.get(pk=1)
            # content = serializer.data.get('content')
            try:
                comment = serializer.save()
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
        return Response(context, status=status.HTTP_204_NO_CONTENT)


class HashTagWrite(APIView):
    
    def post(self, request, post_id):
        # return Response(request)
        serializer = HashTagSerializer(data=request.data)
        if serializer.is_valid():
            # try:
            #     post = Post.objects.get(pk=post_id)
            # except ObjectDoesNotExist as e:
            #     return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            # # user = request.user
            # user = User.objects.get(pk=1)
            # content = serializer.data.get('content')
            try:
                hashTag = serializer.save()
            except ObjectDoesNotExist as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            context = {
                "post_id": post_id,
            }
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HashTagDelete(View):

    def post(self, request, hashTag_id):
        try:
            hashTag = HashTag.objects.get(pk=hashTag_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        post_id = hashTag.post.pk
        hashTag.delete()
        context = {
            "post_id": post_id,
        }
        return Response(context, status=status.HTTP_204_NO_CONTENT)