import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class UserStatusConsumer(WebsocketConsumer):
	def connect(self):
		self.user = self.scope["user"]
		if self.user.is_authenticated:
			async_to_sync(self.channel_layer.group_add)(
				"online_users",
				self.channel_name
			)
			self.accept()
			self.update_user_status(online=True)

	def disconnect(self, close_code):
		if self.user.is_authenticated:
			async_to_sync(self.channel_layer.group_discard)(
				"online_users",
				self.channel_name
			)
			self.update_user_status(online=False)

	def update_user_status(self, online):
		self.user.is_online = online
		self.user.save()

	# def receive(self, text_data):
	# 	data = json.loads(text_data)
	# 	pass