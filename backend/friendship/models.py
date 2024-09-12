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
		return f"{self.requester.username} -> {self.receiver.username} ({'Accepted' if self.accepted else 'Pending'})"
