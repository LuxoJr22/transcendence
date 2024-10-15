from django.db import models
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from users.serializers import PublicUserSerializer
from .models import Friendship, Block
from .serializers import FriendshipSerializer, CreateFriendshipSerializer, BlockSerializer, CreateBlockSerializer

class SendFriendRequestView(generics.CreateAPIView):
	serializer_class = CreateFriendshipSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		friendship = serializer.save(requester=self.request.user)
		receiver = friendship.receiver
		sender = self.request.user.username

		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
			f"user_{receiver.id}",
			{
				"type": "notify_user",
				"notification_type": "friend_request",
				"message": f"{sender} sent you a friend request",
			}
		)

class AcceptFriendRequestView(generics.UpdateAPIView):
	queryset = Friendship.objects.all()
	serializer_class = FriendshipSerializer
	permission_classes = [IsAuthenticated]

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		if instance.receiver != request.user:
			return Response({"error": "You are not authorized to accept this request"}, status=status.HTTP_403_FORBIDDEN)

		instance.accepted = True
		instance.save()
		return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)

class RejectFriendRequestView(generics.DestroyAPIView):
	queryset = Friendship.objects.all()
	serializer_class = FriendshipSerializer
	permission_classes = [IsAuthenticated]

	def delete(self, request, pk):
		instance = self.get_object()
		if instance.receiver != request.user:
			return Response({"error": "You are not authorized to reject this request"}, status=status.HTTP_403_FORBIDDEN)
		try:
			friendship = Friendship.objects.get(pk=pk, receiver=request.user, accepted=False)
			friendship.delete()
			return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)
		except Friendship.DoesNotExist:
			return Response({"error": "Friend request not found or already accepted"}, status=status.HTTP_404_NOT_FOUND)

class FriendsListView(generics.ListAPIView):
	serializer_class = PublicUserSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		friendships = Friendship.objects.filter(
			(models.Q(requester=self.request.user) | models.Q(receiver=self.request.user)),
			accepted=True
		)
		friends = []
		for friendship in friendships:
			if friendship.requester == self.request.user:
				friends.append(friendship.receiver)
			else:
				friends.append(friendship.requester)
		return friends

class FriendRequestsListView(generics.ListAPIView):
	serializer_class = FriendshipSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Friendship.objects.filter(receiver=self.request.user, accepted=False)

class RemoveFriendshipView(generics.DestroyAPIView):
	serializer_class = FriendshipSerializer
	permission_classes = [IsAuthenticated]

	def delete(self, request, *args, **kwargs):
		user = request.user
		friend_id = kwargs.get('friend_id')

		try:
			friendship = Friendship.objects.get(
				(models.Q(requester=user, receiver__id=friend_id) | models.Q(receiver=user, requester__id=friend_id)),
				accepted=True
			)
			friendship.delete()
			return Response({"message": "Friendship removed"}, status=status.HTTP_200_OK)
		except Friendship.DoesNotExist:
			return Response({"error": "Friendship not found"}, status=status.HTTP_404_NOT_FOUND)

class BlockUserView(generics.CreateAPIView):
	serializer_class = CreateBlockSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		blocker = self.request.user
		blocked = serializer.validated_data['blocked']
		Friendship.objects.filter(
			(models.Q(requester=blocker, receiver=blocked) | models.Q(requester=blocked, receiver=blocker))
		).delete()

		serializer.save(blocker=blocker)

class UnblockUserView(generics.DestroyAPIView):
	serializer_class = BlockSerializer
	permission_classes = [IsAuthenticated]

	def delete(self, request, *args, **kwargs):
		user = request.user
		blocked_id = kwargs.get('blocked_id')

		try:
			block = Block.objects.get(blocker=user, blocked__id=blocked_id)
			block.delete()
			return Response({"message": "User unblocked"}, status=status.HTTP_200_OK)
		except Block.DoesNotExist:
			return Response({"error": "Block not found"}, status=status.HTTP_404_NOT_FOUND)

class BlockedUsersListView(generics.ListAPIView):
	serializer_class = PublicUserSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		blocks = Block.objects.filter(blocker=self.request.user)

		blocked_users = []
		for block in blocks:
			blocked_users.append(block.blocked)
		return blocked_users
