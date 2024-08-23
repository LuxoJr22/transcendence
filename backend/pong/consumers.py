import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from .models import PongGroup

class PongConsumer(WebsocketConsumer):
	def connect(self):
		self.room_group_name = 'test'
		self.user = self.scope['user']
		try:
			self.pongroom = get_object_or_404(PongGroup, group_name=self.room_group_name)
		except:
			self.pongroom = PongGroup.objects.create(
				group_name = self.room_group_name,
			)
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)

		if self.user not in self.pongroom.users_online.all():
			self.pongroom.users_online.add(self.user)

		self.accept()

	def disconnect(self):
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)
		if self.user in self.pongroom.users_online.all():
			self.pongroom.users_online.remove(self.user)


	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		event = text_data_json['event']
		
		
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type':'Pong_event',
				'message':message,
				'event':event,
			}
		)

	def Pong_event(self, event):
		message = event['message']
		event = event['event']

		self.send(text_data=json.dumps({
			'type':'Pong',
			'message':message,
			'event':event,
			'count':self.pongroom.users_online.count()
		}))