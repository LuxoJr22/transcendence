import json
import random
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync



class PongConsumer(WebsocketConsumer):
	def connect(self):
		self.room_group_name = 'test'
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)

		self.accept()


	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		event = text_data_json['event']
		
		
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type':'Pong_event',
				'message':message,
				'event':event
			}
		)

	def Pong_event(self, event):
		message = event['message']
		event = event['event']

		self.send(text_data=json.dumps({
			'type':'Pong',
			'message':message,
			'event':event
		}))