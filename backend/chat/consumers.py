import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from users.models import User
from friendship.models import Block
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.receiver_id = self.scope['url_route']['kwargs']['user_id']
		self.sender = self.scope['user']

		if not self.sender.is_authenticated:
			await self.close()
			return
		if await sync_to_async(lambda: Block.objects.filter(blocker=self.sender, blocked__id=self.receiver_id).exists())():
			await self.close()
			return
		if await sync_to_async(lambda: Block.objects.filter(blocker__id=self.receiver_id, blocked=self.sender).exists())():
			await self.close()
			return

		self.room_group_name = f'chat_{min(self.sender.id, int(self.receiver_id))}_{max(self.sender.id, int(self.receiver_id))}'

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']

		await self.save_message(self.sender, self.receiver_id, message)

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message,
				'sender': self.sender.username
			}
		)
		await self.channel_layer.group_send(
			f'user_{self.receiver_id}',
			{
				'type': 'notify_user',
				'message': f"{self.sender.username}: {message}",
			}
		)

	async def chat_message(self, event):
		message = event['message']
		sender = event['sender']

		await self.send(text_data=json.dumps({
			'message': message,
			'sender': sender
		}))

	@sync_to_async
	def save_message(self, sender, receiver_id, message_content):
		receiver = User.objects.get(id=receiver_id)
		Message.objects.create(sender=sender, receiver=receiver, content=message_content)
