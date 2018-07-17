from django.contrib.auth import get_user_model
from rest_framework import status

from project.api.test.test_master import MasterTestWrapper
from project.feed.models import Friendship


User = get_user_model()


class TestSendFriendRequest(MasterTestWrapper.MasterTest):
    # test for SendFriendRequestView
    endpoint = 'api:send_friend_request'
    methods = ['POST']

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
            'user_id': self.users[1].id
        }

    def test_request_sent(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url(**self.get_kwargs())
        response = self.client.post(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(Friendship.objects.all())
        self.assertIn('Friendship request sent', response.data)

    def test_already_sent(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        Friendship.objects.create(sender=self.user, receiver=self.users[1])
        self.url = self.get_url(**self.get_kwargs())
        response = self.client.post(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(Friendship.objects.all())
        self.assertIn('Already friends or friend request pending', response.data)

    def test_receiver_nonexistant(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        user = User.objects.create_user(username="random", password="123Hello.")
        User.objects.get(id=user.id).delete()
        self.url = self.get_url(user_id=user.id)
        response = self.client.post(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data, {"detail": "Not found."})


class ListOpenFriendRequests(MasterTestWrapper.MasterTest):
    # tests for ListOpenFriendRequestsView --> all request i sent that are still pending
    endpoint = 'api:list_all_friend_requests'

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

    def test_open_sent(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url()
        response = self.client.get(self.url, format='json')
        Friendship.objects.create(sender=self.user, receiver=self.users[1])
        Friendship.objects.create(sender=self.user, receiver=self.users[2])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(Friendship.objects.all())
        self.assertEquals(len(Friendship.objects.filter(sender=self.user)), 2)
        self.assertEquals(len(Friendship.objects.filter(status='pending')), 2)


class TestListPendingFriendRequests(MasterTestWrapper.MasterTest):
    # test ListPendingFriendRequestsView --> all friend requests i received
    endpoint = 'api:pending_requests'

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

    def test_received_pending(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.url = self.get_url()
        response = self.client.get(self.url, format='json')
        Friendship.objects.create(sender=self.users[1], receiver=self.user)
        Friendship.objects.create(sender=self.users[2], receiver=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(Friendship.objects.all())
        self.assertEquals(len(Friendship.objects.filter(receiver=self.user)), 2)
        self.assertEquals(len(Friendship.objects.filter(status='pending')), 2)


class FriendRequestAcceptTest(MasterTestWrapper.MasterTest):
    # test FriendRequestAcceptView
    endpoint = 'api:accept_request'

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
            'request_id': 1
         }
    #
    # def test_status_change(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    #     self.url = self.get_url(**self.get_kwargs())
    #     response = self.client.post(self.url, format='json')
    #     friend = Friendship.objects.create(id=1, status='pending')
    #     friend.status = 'accepted'
    #     friend.save()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEquals(friend.status, 'accepted')

    def test_invalid_request_id(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        friend = Friendship.objects.create(sender=self.users[1], receiver=self.user, status='pending')
        some_id = friend.pk
        friend.delete()
        self.url = self.get_url(request_id=some_id)
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
