from rest_framework import serializers
from .models import Tournament
import re

class TournamentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields = ['id', 'name', 'capacity']
		extra_kwargs = {'id': {'read_only':True},}

	def validate_name(self, value):
		if value:
			if len(value) < 3:
				raise serializers.ValidationError("Username must be at least 3 characters long")
			if len(value) > 32:
				raise serializers.ValidationError("Username must not exceed 32 characters long")
			if not re.match("^[a-zA-Z0-9-._]+$", value):
				raise serializers.ValidationError("Username can only contain letters, numbers, hyphens, dots, and underscores.")
		return value

	def validate_capacity(self, value):
		if value not in [4, 8]:
			raise serializers.ValidationError("Capacity must be either 4 or 8.")
		return value

	def create(self, validated_data):
		tournament = Tournament.objects.create(**validated_data)
		tournament.nb_player = tournament.capacity
		tournament.save()
		return tournament
	
	
class TournamentListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields = ['id', 'name', 'nb_player', 'participants', 'capacity']
