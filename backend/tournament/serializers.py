from rest_framework import serializers
from .models import Tournament

class TournamentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields = ['id', 'name']
		extra_kwargs = {'id': {'read_only':True},}

	def create(self, validated_data):
		tournament = Tournament.objects.create(**validated_data)
		return tournament

class JoinTournamentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields = ['participants']

	def update(self, instance, validated_data):
		user = self.context['request'].user
		instance.participants.add(user)
		instance.save()
		return instance
