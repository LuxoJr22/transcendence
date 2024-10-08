from rest_framework import serializers
from .models import Tournament

class TournamentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields = ['id', 'name', 'nb_player', 'capacity']
		extra_kwargs = {'id': {'read_only':True},}

	def create(self, validated_data):
		tournament = Tournament.objects.create(**validated_data)
		return tournament
	
	
class TournamentListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields = ['id', 'name', 'nb_player', 'participants', 'capacity']

