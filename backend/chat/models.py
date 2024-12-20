from django.db import models
from users.models import User
from django.utils import timezone

class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
	content = models.TextField()
	timestamp = models.DateTimeField(default=timezone.now)

	is_invitation = models.BooleanField(default=False)
	gamemode = models.CharField(max_length=12, null=True, blank=True)
	match_id = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
