from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.serializers.posts import PostSerializer
from project.feed.models import Post, Like


class ListLikedPostsView(APIView):
    def get(self, request):
        posts = Post.objects.filter(likes__user=request.user)
        return Response(PostSerializer(posts, many=True).data)


class PostNewLikeView(APIView):
    def get_object(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
            return post
        except Post.DoesNotExist:
            raise Http404

    def post(self, request, post_id):
        posts = self.get_object(post_id)
        if posts.likes.filter(user=request.user):
            return Response('Already liked')
        Like.objects.create(user=request.user, post=posts)
        return Response('OK')


class PostDislikeView(APIView):
    def get_object(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
            return post
        except Post.DoesNotExist:
            raise Http404

    def post(self, request, post_id):
        posts = self.get_object(post_id)
        if posts.likes.filter(user=request.user):
            Like.objects.get(user=request.user, post=posts).delete()
            return Response('Removed')
        return Response('Nothing changed')
