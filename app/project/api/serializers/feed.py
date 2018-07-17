from project.api.serializers.posts import PostSerializer
from project.api.serializers.users import UserSerializer
from project.feed.models import Post


class FeedDisplaySerializer(PostSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'created', 'user']
        read_only_fields = ['created', 'id', 'user']
