from django.db import models
from users.models import User

class ShooterMatchmaking(models.Model):
	group_name = models.CharField(max_length=128, unique=True)
	users_online = models.ManyToManyField(User, related_name='online_in_shooter_matchmaking', blank=True)

	def __str__(self):
		return self.group_name

class Shooter(models.Model):
	group_name = models.CharField(max_length=128, unique=True)
	users_online = models.ManyToManyField(User, related_name='online_in_shooter_groups', blank=True)

	def __str__(self):
		return self.group_name

class ShooterMatch(models.Model):
	players = models.ManyToManyField(User, related_name='players_in_shooter_match', blank=True)
	winner = models.IntegerField(null=True, blank=True)
	match_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.id
