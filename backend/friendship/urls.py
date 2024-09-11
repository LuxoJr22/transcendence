from django.urls import path
from .views import SendFriendRequestView, AcceptFriendRequestView, FriendsListView, FriendRequestsListView

urlpatterns = [
	path('send/', SendFriendRequestView.as_view(), name='send_friend_request'),
	path('accept/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
	path('friends/', FriendsListView.as_view(), name='friends_list'),
	path('requests/', FriendRequestsListView.as_view(), name='friend_requests'),
]
