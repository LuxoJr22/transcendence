from rest_framework import serializers
from .models import ShooterMatch

class ShooterMatchSerializer(serializers.ModelSerializer):
	class Meta:
		model = ShooterMatch
		fields = [ 'id', 'players', 'elo', 'match_date']
		