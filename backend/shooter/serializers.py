from rest_framework import serializers
from .models import ShooterMatch, PlayerScore

class PlayerScoreSerializer(serializers.ModelSerializer):
	class Meta:
		model = PlayerScore
		fields = ['player_id', 'score']

class ShooterMatchSerializer(serializers.ModelSerializer):
	scores = PlayerScoreSerializer(many=True)

	class Meta:
		model = ShooterMatch
		fields = [ 'id', 'players', 'scores', 'winner', 'elo', 'match_date']
