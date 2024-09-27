from rest_framework import generics
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
		user = self.request.user
		return PongMatch.objects.filter(models.Q(player1=user.id) | models.Q(player2=user.id))
	
	def list(self, request, *args, **kwargs):
		queryset = sorted(
			self.get_queryset(),
			key=lambda match: match.match_date,
			reverse=True
		)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

class SkinsView(generics.RetrieveAPIView):
	serializer_class = PongMatchSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		game_id = kwargs.get('game_id')
		try:
			match = PongMatch.objects.get(id=game_id)
			player1_skin = User.objects.get(id=match.player1).skin
			player2_skin = User.objects.get(id=match.player2).skin
			return Response({
				'player1':{
					'id': match.player1,
					'skin': player1_skin
				},
				'player2':{
					'id': match.player2,
					'skin': player2_skin
				}
			})
		except PongMatch.DoesNotExist:
			return Response({'error': 'Match not found'}, status=404)
		except User.DoesNotExist:
			return Response({'error': 'User not found'}, status=404)
