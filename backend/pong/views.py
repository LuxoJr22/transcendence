from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import models
from .models import PongMatch
from .serializers import PongMatchSerializer
from users.models import User

class PongMatchHistoryView(generics.ListAPIView):
	serializer_class = PongMatchSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user_id = self.kwargs['user_id']
		user = generics.get_object_or_404(User, id=user_id)
		return PongMatch.objects.filter(
			(models.Q(player1=user.id) | models.Q(player2=user.id)) & models.Q(winner__isnull=False)
		)
	
	def list(self, request, *args, **kwargs):
		queryset = sorted(
			self.get_queryset(),
			key=lambda match: match.match_date,
			reverse=True
		)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

class SkinsView(generics.RetrieveAPIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		game_id = kwargs.get('game_id')
		try:
			match = PongMatch.objects.get(id=game_id)
			player1 = User.objects.get(id=match.player1)
			player2 = User.objects.get(id=match.player2)
			return Response({
				'player1':{
					'id': match.player1,
					'username': player1.username,
					'skin': player1.skin
				},
				'player2':{
					'id': match.player2,
					'username': player2.username,
					'skin': player2.skin
				}
			}, status=status.HTTP_200_OK)
		except PongMatch.DoesNotExist:
			return Response({'error': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)
		except User.DoesNotExist:
			return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
		
class SettingsView(generics.RetrieveAPIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		user_id = kwargs.get('user_id')
		try:
			user = User.objects.get(id=user_id)
			return Response({
				'settings': user.settings.pong
			}, status=status.HTTP_200_OK)
		except User.DoesNotExist:
			return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)