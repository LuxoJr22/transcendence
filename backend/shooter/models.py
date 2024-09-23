from django.db import models
from users.models import User

class Shooter(models.Model):
	group_name = models.CharField(max_length=128, unique=True)
	users_online = models.ManyToManyField(User, related_name='online_in_shooter_groups', blank=True)

	def __str__(self):
		return self.group_name
