from rest_framework import serializers
from django.db import models
from .models import Message
from users.serializers import PublicUserSerializer

class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ['id', 'sender', 'receiver', 'content', 'is_invitation', 'gamemode', 'match_id', 'timestamp']

class ChatHistorySerializer(PublicUserSerializer):
	last_message = serializers.SerializerMethodField()

	class Meta(PublicUserSerializer.Meta):
		fields = PublicUserSerializer.Meta.fields + ['last_message']

	def get_last_message(self, user):
		request_user = self.context['request'].user

		last_message = Message.objects.filter(
			models.Q(sender=request_user, receiver=user) | models.Q(sender=user, receiver=request_user)
		).order_by(
			'-timestamp'
		).first()

		if last_message:
			return {
				'sender': last_message.sender.id,
				'content': last_message.content,
				'timestamp': last_message.timestamp
			}
		return None
