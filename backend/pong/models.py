from django.db import models
from users.models import User

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
	player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_player1')
	player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_player2')
	winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='matches_won')
	match_date = models.DateTimeField()

	def __str__(self):
		return self.name
