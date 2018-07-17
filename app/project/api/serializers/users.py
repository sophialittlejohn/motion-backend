from django.contrib.auth import get_user_model
from rest_framework import serializers

from project.feed.models import Post, Profile

User = get_user_model()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        label='id',
    )
    username = serializers.CharField(
        label='username',
    )
    post_count = serializers.IntegerField(
        label='post count',
        read_only=True,
    )
    fame_index = serializers.IntegerField(
        label='fame index',
        read_only=True,
    )
    pic = serializers.SerializerMethodField(
        label='profile_pic',
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'post_count', 'fame_index', 'followers_count']
        read_only_fields = fields

    def get_pic(self, user):
        if user.user_profile.profile_pic:
            return user.user_profile.profile_pic.url
        return "Nope"

    def to_representation(self, user):
        data = super().to_representation(user)
        return {
            **data,
            'post_count': user.posts.count(),
            # takes the likes from each post and creates a list and then sums up the list for total likes
            'fame_index': sum([p.likes.count() for p in user.posts.all()]),
            'followers_count': user.followers.count(),
        }


class UserPrivateInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        label='id',
        read_only=True,
    )
    username = serializers.CharField(
        label='username',
    )
    first_name = serializers.CharField(
        label='first name'
    )
    last_name = serializers.CharField(
        label='last name'
    )
    email = serializers.EmailField(
        label='email'
    )

    class Meta:
        model = Profile
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


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
