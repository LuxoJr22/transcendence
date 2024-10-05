from rest_framework import serializers
from .models import PongMatch

class PongMatchSerializer(serializers.ModelSerializer):
	class Meta:
		model = PongMatch
		fields = ['id', 'player1', 'player2', 'type', 'gamemode', 'score1', 'score2' 'winner', 'match_date']
