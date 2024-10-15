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
			async_to_sync(self.channel_layer.group_add)(
				f"user_{self.user.id}",
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
			async_to_sync(self.channel_layer.group_discard)(
				f"user_{self.user.id}",
				self.channel_name
			)
			self.update_user_status(online=False)

	def update_user_status(self, online):
		self.user.is_online = online
		self.user.save(update_fields=['is_online'])

	def notify_user(self, event):
		notification_type = event["notification_type"]
		if (notification_type != "tournament"):
			self.send(text_data=json.dumps({
				"type": notification_type,
				"message": event["message"],
			}))
		else:
			self.send(text_data=json.dumps({
				"type": notification_type,
				"message": event["message"],
				"tournament": event["tournament"],
			}))
