from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Shooter, ShooterMatchmaking, ShooterMatch
from .serializers import ShooterMatchSerializer
from django.db import models
from users.models import User

import sys

# Create your views here.

class ShooterMatchMakingView(generics.CreateAPIView):
	permission_classes = [IsAuthenticated]
	def post(self, request):
		self.user = self.request.user
		Matchs = list(ShooterMatch.objects.filter(
			models.Q(elo__gte=self.user.shooter_elo-150) & 
			models.Q(elo__lte=self.user.shooter_elo+150) &
			models.Q(winner=None)))
		for game in Matchs:
			if game.players.filter(id=self.user.id):
				return (Response({
					'match':game.id
				}))
			if game.players.count() >= 4:
				Matchs.remove(game)
		if (len(Matchs) == 0):
			self.shootermatch = ShooterMatch.objects.create(
					elo = self.user.shooter_elo)
			self.shootermatch.room_name = f'shooter_{self.shootermatch.id}'
			self.shootermatch.players.set([self.user])
			self.shootermatch.save()
		else:
			self.shootermatch = Matchs[0]
			self.shootermatch.players.add(self.user)
			self.shootermatch.save()
		return (Response({
			'match':self.shootermatch.id
		}))
	
class ShooterSettingsView(generics.RetrieveAPIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		user_id = kwargs.get('user_id')
		try:
			user = User.objects.get(id=user_id)
			return Response({
				'settings': user.settings.shooter
			}, status=status.HTTP_200_OK)
		except User.DoesNotExist:
			return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)