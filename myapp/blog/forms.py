from django import forms
from .models import Post, Comment, HashTag


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'cols': 50})
        }


class HashTagForm(forms.ModelForm):

    class Meta:
        model = HashTag
        fields = ['name']