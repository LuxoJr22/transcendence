from django.db import models
from users.models import User

class Friendship(models.Model):
	requester = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
	receiver = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
	accepted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('requester', 'receiver')

	def __str__(self):
		return f"{self.requester.username}'s friendrequest to {self.receiver.username} ({'Accepted' if self.accepted else 'Pending'})"

class Block(models.Model):
	blocker = models.ForeignKey(User, related_name='blocks_sent', on_delete=models.CASCADE)
	blocked = models.ForeignKey(User, related_name='blocks_received', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('blocker', 'blocked')

	def __str__(self):
		return f"{self.blocker.username} blocked {self.blocked.username}"
