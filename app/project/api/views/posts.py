from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.serializers.posts import PostSerializer

from project.feed.models import Post


User = get_user_model()


class PostUpdateGetDeleteView(APIView):
    def get_object(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
            return post
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_id):
        post = self.get_object(post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def post(self, request, post_id):
        # updates a specific post by post_id
        post = self.get_object(post_id)
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, post_id):
        post = self.get_object(post_id)
        post.delete()
        return Response("OK")


class NewPostView(APIView):
    def send_email(self, email, sender):
        message = EmailMessage(
            subject='Your Friend has a new post',
            body=f'{sender} created a new post.',
            to=[email],
        )
        message.send()

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = Post.objects.create(
            content=serializer.validated_data.get('content'),
            user=request.user,
        )
        friends = User.objects.filter(Q(
            Q(friend_request__receiver=request.user) | Q(friend_request__status='accepted') |
            Q(friend_requested__sender=request.user) | Q(friend_requested__status='accepted')
        ))
        for friend in friends:
            self.send_email(friend.email, request.user.username)
        return Response(PostSerializer(post).data)


class SharePostView(APIView):
    def post(self, request, post_id):
        pass
