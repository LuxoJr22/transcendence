from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField

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

class PlayerScore(models.Model):
	player_id = models.IntegerField()
	score = models.IntegerField(default=0)

	def __str__(self):
		return f'{self.player_id}: {self.score}'

class ShooterMatch(models.Model):
	players = models.ManyToManyField(User, related_name='players_in_shooter_match')
	scores = models.ManyToManyField(PlayerScore, related_name='scores_in_shooter_match', blank=True)
	room_name = models.CharField(max_length=128, unique=True, blank=True)
	winner = models.IntegerField(null=True, blank=True)
	elo = models.IntegerField()
	match_date = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.id
