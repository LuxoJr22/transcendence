from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated

class MessageListView(generics.ListAPIView):
	serializer_class = MessageSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		sender = self.request.user
		receiver_username = self.kwargs['username']
		return Message.objects.filter(sender=sender, receiver__username=receiver_username) | \
				Message.objects.filter(sender__username=receiver_username, receiver=sender)
