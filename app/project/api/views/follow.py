from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.serializers.users import UserSerializer
from project.feed.models import Profile

User = get_user_model()


class UserFollowerView(APIView):
    def get(self, request):
        users = User.objects.filter(user_profile__followees=request.user)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class FollowingUserView(APIView):
    # get users I'm following
    def get(self, request):
        followers = request.user.user_profile.followees.all()
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)


class FollowUserView(APIView):
    # follow a user
    def get_object(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            raise Http404

    def send_email(self, email, sender):
        # sender = sender.username
        message = EmailMessage(
            subject='You have a new follower',
            body=f'{sender} started following you.',
            to=[email],
        )
        message.send()

    def post(self, request, user_id):
        user = self.get_object(user_id)
        user_profile, created = Profile.objects.get_or_create(user=request.user)
        user_profile.followees.add(user)
        serializer = UserSerializer(user)
        self.send_email(user.email, request.user.username)
        return Response(serializer.data)


class UnfollowUserView(APIView):
    # unfollow user
    def get_object(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            raise Http404

    def post(self, request, user_id):
        user = self.get_object(user_id)
        user_profile, created = Profile.objects.get_or_create(user=request.user)
        user_profile.followees.remove(user)
        serializer = UserSerializer(user)
        return Response(serializer.data)
