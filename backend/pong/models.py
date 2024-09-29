from django.db import models
from users.models import User
from django.utils import timezone

class PongMatchmaking(models.Model):
	group_name = models.CharField(max_length=128, unique=True)
	users_online = models.ManyToManyField(User, related_name='online_in_pong_matchmaking', blank=True)

	def __str__(self):
		return self.group_name

class PongGroup(models.Model):
	group_name = models.CharField(max_length=128, unique=True)
	users_online = models.ManyToManyField(User, related_name='online_in_pong_groups', blank=True)

	def __str__(self):
		return self.group_name

class PongMatch(models.Model):
	player1 = models.IntegerField()
	player2 = models.IntegerField()
	type = models.CharField(max_length=128)
	gamemode = models.CharField(max_length=128)
	winner = models.IntegerField(null=True, blank=True)
	match_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.id
