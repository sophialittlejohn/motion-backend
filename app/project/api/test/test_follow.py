from django.contrib.auth import get_user_model
from rest_framework import status

from project.api.test.test_master import MasterTestWrapper


User = get_user_model()


class FollowUserTest(MasterTestWrapper.MasterTest):
    # test FollowUserView
    endpoint = 'api:following_user'
    methods = ['POST']
    kwargs = {
        'user_id': 1,
    }

    def setUp(self):
        super().setUp()
        self.users = []
        for i in range(3):
            self.users.append(
                User.objects.create_user(
                    username=f'user{i}',
                    password=f'super_secure_{i}',
                )
            )

    def get_kwargs(self):
        return {
            'user_id': self.users[0].id
        }

    def test_follow_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(**self.get_kwargs())
        response = self.client.post(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_number_of_followers(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(**self.get_kwargs())
        response = self.client.post(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.user.user_profile, 10)
        self.assertEquals(self.user.user_profile.followees.count(), 1)

    def test_user_already_followed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(**self.get_kwargs())
        response = self.client.post(self.url, {}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_nonexistent(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(user_id=50)
        response = self.client.post(self.url, {}, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


# class UnfollowUserTest(MasterTestWrapper.MasterTest):
#     endpoint = 'api:unfollowing_user'
#     methods = ['POST']
#     kwargs = {'user_id': 2}
#
#     def setUp(self):
#         super().setUp()
#         self.users = []
#         for i in range(3):
#             self.users.append(
#                 User.objects.create_user(
#                     username=f'user{i}',
#                     password=f'super_secure_{i}',
#                 )
#             )
#         user_profile = UserProfile()
#         self.users[0].user_profile = user_profile
#         self.users[1].user_profile = user_profile
#         follower = self.users[0].user_profile.followees.add(self.users[1])
#
#     def test_unfollow_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
#         self.url = self.get_url(**self.get_kwargs())
#         response = self.client.post(self.url, format='json')
#         self.assertEquals(response.status_code, status.HTTP_200_OK)
