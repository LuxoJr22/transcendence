from django.db import models
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Friendship
from .serializers import FriendshipSerializer, CreateFriendshipSerializer

class SendFriendRequestView(generics.CreateAPIView):
	serializer_class = CreateFriendshipSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(requester=self.request.user)

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
		return Response({"message": "Friend request accepted"})

class FriendsListView(generics.ListAPIView):
	serializer_class = FriendshipSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Friendship.objects.filter(
			(models.Q(requester=self.request.user) | models.Q(receiver=self.request.user)),
			accepted=True
		)

class FriendRequestsListView(generics.ListAPIView):
	serializer_class = FriendshipSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Friendship.objects.filter(receiver=self.request.user, accepted=False)
