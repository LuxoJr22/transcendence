from django.db import models
from django.utils import timezone
from users.models import User
from pong.models import PongMatch

class Tournament(models.Model):
	name = models.CharField(max_length=100, unique=True)
	participants = models.ManyToManyField(User, related_name='participants')
	matchs = models.ManyToManyField(PongMatch, related_name='matchs')
	last_round = models.DateTimeField(null=True, blank=True)
	nb_player = models.IntegerField()

	is_full = models.BooleanField(default=False)

	def __str__(self):
		return self.name