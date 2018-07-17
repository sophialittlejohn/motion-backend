from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from project.feed.models import Post


User = get_user_model()


class MasterTestWrapper:
    class MasterTest(APITestCase):
        # this gets called every time we run a test
        endpoint = None
        methods = []
        kwargs = {}

        def setUp(self):
            self.user = User.objects.create_user(
                username='test user',
                password='super secure',
            )
            self.post = Post.objects.create(
                user=self.user,
                content='Test content!',
            )
            self.refresh = RefreshToken.for_user(self.user)
            self.access_token = self.refresh.access_token

        def get_kwargs(self):
            return self.kwargs

        def get_url(self, *args, **kwargs):
            return reverse(self.endpoint, args=args, kwargs=kwargs)

        def test_unauthorized_requests(self):
            url = self.get_url(**self.get_kwargs())
            for m in self.methods:
                try:
                    method = getattr(self.client, m.lower())
                    response = method(url)
                    if response:
                        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
                except AttributeError:
                    raise Exception(f"No such method {m}")
