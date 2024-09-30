from rest_framework import serializers
from .models import PongMatch

class PongMatchSerializer(serializers.ModelSerializer):
	class Meta:
		model = PongMatch
		fields = ['id', 'player1', 'player2', 'type', 'gamemode', 'winner', 'match_date']
