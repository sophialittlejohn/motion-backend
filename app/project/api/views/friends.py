from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.serializers.friends import FriendRequestSerializer
from project.api.serializers.users import UserSerializer
from project.feed.models import Friendship

User = get_user_model()


class SendFriendRequestView(APIView):
    def get_object(self, user_id):
        try:
            receiver = User.objects.get(id=user_id)
            return receiver
        except User.DoesNotExist:
            raise Http404

    def send_email(self, email, sender):
        message = EmailMessage(
            subject='You have a new friend request',
            body=f'{sender} requested to be your friend.',
            to=[email],
        )
        message.send()

    def post(self, request, user_id):
        receiver = self.get_object(user_id)
        if Friendship.objects.filter(sender=request.user, receiver=receiver):
            return Response('Already friends or friend request pending')
        if Friendship.objects.filter(sender=receiver):
            return Response('You can\'t friend yourself')
        Friendship.objects.create(sender=request.user, receiver=receiver)
        self.send_email(receiver.email, request.user.username)
        return Response('Friendship request sent')


class ListOpenFriendRequestsView(GenericAPIView):
    serializer_class = FriendRequestSerializer

    def get(self, request):
        # list all friend requests I sent that are still pending
        try:
            requests = Friendship.objects.filter(receiver=request.user, status='pending')
        except Friendship.DoesNotExist:
            raise Http404
        serializer = self.get_serializer(requests, many=True)
        return Response(serializer.data)


class ListPendingFriendRequestsView(GenericAPIView):
    serializer_class = FriendRequestSerializer

    def get(self, request):
        # list all friend requests sent to me and pending
        try:
            requests = Friendship.objects.filter(sender=request.user, status='pending')
        except Friendship.DoesNotExist:
            raise Http404
        serializer = self.get_serializer(requests, many=True)
        return Response(serializer.data)


class FriendRequestAcceptView(GenericAPIView):
    # accept a friend request sent to me
    serializer_class = FriendRequestSerializer

    def send_email(self, email, receiver):
        message = EmailMessage(
            subject='Friend request accepted',
            body=f'{receiver} has accepted your friend request.',
            to=[email],
        )
        message.send()

    def post(self, request, request_id):
        try:
            requester = Friendship.objects.get(id=request_id, status='pending')
        except Friendship.DoesNotExist:
            raise Http404
        if requester.receiver == request.user:
            requester.status = 'accepted'
            requester.save()
            self.send_email(requester.sender.email, requester.receiver.username)
            return Response('OK')
        return Response('You may not do that!')


class FriendRequestRejectView(GenericAPIView):
    # reject a friend request sent to me
    serializer_class = FriendRequestSerializer

    def post(self, request, request_id):
        try:
            requester = Friendship.objects.get(id=request_id, status='pending')
        except Friendship.DoesNotExist:
            raise Http404
        if requester.receiver == request.user:
            requester.status = 'declined'
            requester.save()
            return Response('OK')
        return Response('You may not do that!')


class UnfriendView(APIView):
    serializer_class = UserSerializer

    def delete(self, request, request_id):
        try:
            record = Friendship.objects.get(id=request_id)
        except Friendship.DoesNotExist:
            raise Http404
        if record.sender == request.user or record.receiver == request.user:
            record.delete()
            return Response('OK')
        return Response("Nope")


class ListAllFriends(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        return Response(UserSerializer(
            User.objects.filter(Q(
                Q(friend_request__receiver=request.user) | Q(friend_request__status='accepted') |
                Q(friend_requested__sender=request.user) | Q(friend_requested__status='accepted')
                )),
            many=True).data)
