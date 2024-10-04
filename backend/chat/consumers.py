import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from users.models import User
from friendship.models import Block
from pong.models import PongMatch
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

		if 'invite_pong' in text_data_json:
			gamemode = text_data_json['gamemode']
			message = "Invitation to play Pong!" if gamemode == "pong" else "Invitation to play Pong Retro!"

			pong_match = await sync_to_async(PongMatch.objects.create)(
				player1=self.sender.id,
				player2=self.receiver_id,
				type="private",
				gamemode=gamemode
			)

			await self.save_message(self.sender, self.receiver_id, message, is_invitation=True, match_id=pong_match.id, gamemode=gamemode)
			await self.channel_layer.group_send(
				self.room_group_name,
				{
					'type': 'pong_invitation',
					'message': message,
					'sender': self.sender.username,
					'match_id': pong_match.id,
					'gamemode': gamemode
				}
			)
		else:
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

	async def pong_invitation(self, event):
		message = event['message']
		sender = event['sender']
		match_id = event['match_id']
		gamemode = event['gamemode']

		await self.send(text_data=json.dumps({
			'message': message,
			'sender': sender,
			'match_id': match_id,
			'gamemode': gamemode
		}))

	@sync_to_async
	def save_message(self, sender, receiver_id, message, is_invitation=False, match_id=None, gamemode=None):
		receiver = User.objects.get(id=receiver_id)
		Message.objects.create(
			sender=sender,
			receiver=receiver,
			content=message,
			is_invitation=is_invitation,
			match_id=match_id,
			gamemode=gamemode
		)
