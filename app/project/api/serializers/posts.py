from rest_framework import serializers

from project.api.serializers.users import UserSerializer
from project.feed.models import Post


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'created', 'user']
        read_only_fields = ['created', 'id', 'user']

    def to_representation(self, post):
        data = super().to_representation(post)
        return {
            **data,
            'likes_count': post.likes.count(),
        }

    def update(self, post, validated_data):
        content = validated_data.get('content')
        post.content = content
        post.save()
        return post
