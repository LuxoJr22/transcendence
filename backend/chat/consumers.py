import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from users.models import User
from .models import Message

import sys # tmp

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.receiver = self.scope['url_route']['kwargs']['username']
		self.sender = self.scope['user']

		print(self.sender, file=sys.stderr)
		print(self.receiver, file=sys.stderr)

		if not self.sender.is_authenticated:
			await self.close()
			return

		self.room_group_name = f'chat_{self.sender.username}_{self.receiver}'

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		await self.accept()
		print("Connected", file=sys.stderr)

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']

		# Sauvegarder le message dans la base de données
		await self.save_message(self.sender, self.receiver, message)

		# Envoyer le message au groupe
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message,
				'sender': self.sender.username
			}
		)

	async def chat_message(self, event):
		message = event['message']
		sender = event['sender']

		# Envoyer le message au WebSocket
		await self.send(text_data=json.dumps({
			'message': message,
			'sender': sender
		}))

	@sync_to_async
	def save_message(self, sender, receiver_username, message_content):
		receiver = User.objects.get(username=receiver_username)
		Message.objects.create(sender=sender, receiver=receiver, content=message_content)
