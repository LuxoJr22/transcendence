from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import models
from django.db.models import Max
from .models import Message
from .serializers import MessageSerializer, ChatHistorySerializer
from users.models import User

class MessageListView(generics.ListAPIView):
	serializer_class = MessageSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		sender = self.request.user
		receiver_id = self.kwargs['user_id']
		return Message.objects.filter(sender=sender, receiver__id=receiver_id) | \
				Message.objects.filter(sender__id=receiver_id, receiver=sender)

class ChatHistoryView(generics.ListAPIView):
	serializer_class = ChatHistorySerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user

		last_message_subquery = Message.objects.filter(
			models.Q(sender=user) | models.Q(receiver=user)
		).values(
			'sender', 'receiver'
		).annotate(
			last_message=Max('timestamp')
		).order_by(
			'-last_message'
		)

		partner_ids = set()
		for message in last_message_subquery:
			if message['sender'] == user.id:
				partner_ids.add(message['receiver'])
			else:
				partner_ids.add(message['sender'])

		return User.objects.filter(id__in=partner_ids)

	def list(self, request, *args, **kwargs):
		queryset = sorted(
			self.get_queryset(),
			key=lambda user: Message.objects.filter(
				models.Q(sender=user) | models.Q(receiver=user)
			).aggregate(last_message=Max('timestamp'))['last_message'],
			reverse=True
		)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)
