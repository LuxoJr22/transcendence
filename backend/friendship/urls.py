from django.urls import path
from .views import SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, FriendsListView, FriendRequestsListView, RemoveFriendshipView, BlockUserView, UnblockUserView

urlpatterns = [
	path('send/', SendFriendRequestView.as_view(), name='send_friend_request'),
	path('accept/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
	path('reject/<int:pk>/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
	path('friends/', FriendsListView.as_view(), name='friends_list'),
	path('requests/', FriendRequestsListView.as_view(), name='friend_requests'),
	path('remove/<int:friend_id>/', RemoveFriendshipView.as_view(), name='remove_friendship'),
	path('block/', BlockUserView.as_view(), name='block_user'),
	path('unblock/<int:blocked_id>/', UnblockUserView.as_view(), name='unblock_user'),
]
