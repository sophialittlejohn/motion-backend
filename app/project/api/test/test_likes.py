from rest_framework import status

from project.api.test.test_master import MasterTestWrapper
from project.feed.models import Post, Like


class NewLikeTest(MasterTestWrapper.MasterTest):
    endpoint = 'api:post_new_like'

    def get_kwargs(self):
        return {'post_id': self.post.id}

    def test_post_new_like(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(**self.get_kwargs())
        response = self.client.post(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, 'OK')
        self.assertIsNotNone(Like.objects.get(post=self.post.id))

    def test_already_liked(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        Like.objects.create(user=self.user, post=self.post)
        self.url = self.get_url(**self.get_kwargs())
        response = self.client.post(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, 'Already liked')

    def test_post_nonexistent(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(post_id=99999)
        response = self.client.post(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data, {"detail": "Not found."})


class DislikePostTest(MasterTestWrapper.MasterTest):
    endpoint = 'api:post_dislike'

    def get_kwargs(self):
        return {'post_id': self.post.id}

    def test_post_disliked(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        Like.objects.create(user=self.user, post=self.post)
        self.url = self.get_url(**self.get_kwargs())
        response = self.client.post(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, 'Removed')
        self.assertFalse(Like.objects.all())

    def test_post_already_disliked(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(**self.get_kwargs())
        response = self.client.post(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, "Nothing changed")
        self.assertIsNotNone(Like.objects.all())

    def test_post_nonexistant(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        post = Post.objects.create(content='non existant content', user=self.user)
        post_id = post.id
        post.delete()
        self.url = self.get_url(post_id=post_id)
        response = self.client.post(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
