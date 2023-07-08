from rest_framework import serializers
from .models import Post, Comment, HashTag


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ['content']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request and request.method == 'POST':
            fields_to_remove = set(fields.keys()) - {'content'}
            for field in fields_to_remove:
                fields.pop(field)
        return fields


class HashTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = HashTag
        fields = '__all__'