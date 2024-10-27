import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class UserStatusConsumer(WebsocketConsumer):
	connection_counts = {}

	def connect(self):
		self.user = self.scope["user"]
		if self.user.is_authenticated:
			if self.user.id not in self.connection_counts:
				self.connection_counts[self.user.id] = 0
			self.connection_counts[self.user.id] += 1
			async_to_sync(self.channel_layer.group_add)(
				"online_users",
				self.channel_name
			)
			async_to_sync(self.channel_layer.group_add)(
				f"user_{self.user.id}",
				self.channel_name
			)
			self.accept()
			self.update_user_status()
			# self.group_send("online_users", {
			# 	"type": "user_online",
			# 	"user_id": self.user.id,
			# 	"online": True
			# })

	def disconnect(self, close_code):
		if self.user.is_authenticated:
			self.connection_counts[self.user.id] -= 1
			async_to_sync(self.channel_layer.group_discard)(
				"online_users",
				self.channel_name
			)
			async_to_sync(self.channel_layer.group_discard)(
				f"user_{self.user.id}",
				self.channel_name
			)
			self.update_user_status()
			# self.group_send("online_users", {
			# 	"type": "user_online",
			# 	"user_id": self.user.id,
			# 	"online": False
			# })

	def update_user_status(self):
		if self.connection_counts[self.user.id] == 0:
			online = False
		else:
			online = True
		self.user.is_online = online
		self.user.save(update_fields=['is_online'])

	def notify_user(self, event):
		self.send(text_data=json.dumps({
			"type": event["notification_type"],
			"message": event["message"],
			"info": event["info"]
		}))
