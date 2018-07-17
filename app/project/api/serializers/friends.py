from rest_framework import serializers

from project.api.serializers.users import UserSerializer
from project.feed.models import Friendship


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'sender', 'receiver', 'status']
        read_only_fields = fields
