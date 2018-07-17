from rest_framework import status

from project.api.test.test_master import MasterTestWrapper
from project.feed.models import Post


class TestPostUpdateGetDeleteView(MasterTestWrapper.MasterTest):
    methods = ['GET', 'POST', 'DELETE']
    endpoint = 'api:post_UGD'

    def get_kwargs(self):
        return {'post_id': self.post.id}

    def test_get_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(**self.get_kwargs())
        response = self.client.get(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 5)
        self.assertEquals(response.data.get('content'), 'Test content!')

    def test_nonexistent_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = self.get_url(post_id=30)
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(**self.get_kwargs())
        response = self.client.post(self.url, {'content': 'new updated post'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 5)
        self.assertEquals(Post.objects.get().content, 'new updated post')

    def test_no_content_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(**self.get_kwargs())
        response = self.client.post(self.url, {}, format='json')
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(**self.get_kwargs())
        response = self.client.delete(self.url, {}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Post.objects.count(), 0)

    def test_nonexistent_post_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        post = Post.objects.create(content='non existant content', user=self.user)
        post_id = post.id
        post.delete()
        self.url = self.get_url(post_id=post_id)
        response = self.client.delete(self.url, {}, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(Post.objects.count(), 1)


class PostNew(MasterTestWrapper.MasterTest):
    endpoint = 'api:post_new'
    methods = ['POST']

    def test_new_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # test if new content is being posted
        self.url = self.get_url(**self.kwargs)
        response = self.client.post(self.url, {'content': 'new test post'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Post.objects.count(), 2)
        assert Post.objects.get(content='new test post')

    def test_newpost_no_content(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(**self.kwargs)
        response = self.client.post(self.url, {'content': ''}, format='json')
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be blank.", response.data.get('content'))

    def test_newpost_no_params(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(**self.kwargs)
        response = self.client.post(self.url, {}, format='json')
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", response.data.get('content'))
