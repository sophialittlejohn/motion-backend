from rest_framework import status

from project.api.test.test_master import MasterTestWrapper


class GetFeedTest(MasterTestWrapper.MasterTest):
    methods = ['GET']
    endpoint = 'api:feed_display_view'

    def test_get_feed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = self.get_url()
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data[0].get('content'), 'Test content!')


class GetUserFeedTest(MasterTestWrapper.MasterTest):
    # methods = ['GET']
    endpoint = 'api:feed_display_user_view'

    def get_kwargs(self):
        return {'user_id': self.user.id}

    def test_post_feed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = self.get_url(**self.get_kwargs())
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data[0].get('content'), 'Test content!')
