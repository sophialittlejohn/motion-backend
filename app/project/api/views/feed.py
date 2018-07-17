from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from project.api.serializers.feed import FeedDisplaySerializer
from project.feed.models import Post


class FeedDisplayView(GenericAPIView):
    serializer_class = FeedDisplaySerializer

    def get(self, request, format=None):
        search = request.query_params.get('search')
        if search:
            posts = Post.objects.filter(content__contains=search)
        else:
            posts = Post.objects.all()
        # the Serializer class takes an argument data that needs to be converted into a dict for passing in
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class FeedDisplayUserView(GenericAPIView):
    serializer_class = FeedDisplaySerializer
    queryset = Post.objects.all()

    # def get_queryset(self, **kwargs):
    #     return self.queryset.filter(user=kwargs.get('user'))

    def get(self, request, user_id):
        posts = Post.objects.filter(user_id=user_id)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


