from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from project.api.views.feed import FeedDisplayView, FeedDisplayUserView
from project.api.views.follow import UserFollowerView, FollowingUserView, FollowUserView, \
    UnfollowUserView
from project.api.views.friends import SendFriendRequestView, ListOpenFriendRequestsView, \
    ListPendingFriendRequestsView, FriendRequestAcceptView, FriendRequestRejectView, \
    UnfriendView, ListAllFriends
from project.api.views.likes import ListLikedPostsView, PostNewLikeView, PostDislikeView
from project.api.views.posts import PostUpdateGetDeleteView, NewPostView

from project.api.views import registration
from project.api.views.registration import PasswordResetView, PasswordResetValidate
from project.api.views.user import ListUsersView, UserByIdView, GetUpdateUserProfile

app_name = 'api'

urlpatterns = [
    path('me/', GetUpdateUserProfile.as_view(), name='get_user_profile'),

    path('users/followers/', UserFollowerView.as_view(), name='user_follower_view'),
    path('users/', ListUsersView.as_view(), name='list_users_view'),
    path('users/<int:user_id>/', UserByIdView.as_view(), name='user_by_id'),
    path('users/following/', FollowingUserView.as_view(), name='following_user_view'),
    path('users/follow/<int:user_id>/', FollowUserView.as_view(), name='following_user'),
    path('users/unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollowing_user'),
    path('users/friendrequest/<int:user_id>/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('users/friendrequests/', ListOpenFriendRequestsView.as_view(), name='list_all_friend_requests'),
    path('users/friendrequests/pending/', ListPendingFriendRequestsView.as_view(), name='pending_requests'),
    path('users/friendrequests/accept/<int:request_id>/', FriendRequestAcceptView.as_view(),
         name='accept_request'),
    path('users/friendrequests/reject/<int:request_id>/', FriendRequestRejectView.as_view(),
         name='reject_request'),
    path('users/unfriend/<int:request_id>/', UnfriendView.as_view(), name='unfriend_user'),
    path('users/friends/', ListAllFriends.as_view(), name='list_all_friends'),

    path('feed/', FeedDisplayView.as_view(), name='feed_display_view'),
    path('feed/<int:user_id>/', FeedDisplayUserView.as_view(), name='feed_display_user_view'),

    path('posts/<int:post_id>/', PostUpdateGetDeleteView.as_view(), name='post_UGD'),
    path('posts/new-post/', NewPostView.as_view(), name='post_new'),
    path('posts/likes/', ListLikedPostsView.as_view(), name='liked_post_view'),
    path('posts/<int:post_id>/like/', PostNewLikeView.as_view(), name='post_new_like'),
    path('posts/<int:post_id>/dislike/', PostDislikeView.as_view(), name='post_dislike'),
    # path('posts/share-post/<int:post_id>/', SharePostView.as_view(), name='share_post'),

    path('registration/', registration.RegistrationView.as_view(), name='registration_view'),
    path('registration/validation/', registration.RegistrationValidationView.as_view(),
         name='registration_validation_view'),

    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('auth/password-reset/validate/', PasswordResetValidate.as_view(), name='pw_reset_validate'),
]
