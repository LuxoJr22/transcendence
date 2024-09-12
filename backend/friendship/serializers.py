from rest_framework import serializers
from .models import Friendship
from users.serializers import PublicUserSerializer

class FriendshipSerializer(serializers.ModelSerializer):
	requester = PublicUserSerializer(read_only=True)
	receiver = PublicUserSerializer(read_only=True)

	class Meta:
		model = Friendship
		fields = ['id', 'requester', 'receiver', 'accepted', 'created_at']

class CreateFriendshipSerializer(serializers.ModelSerializer):
	class Meta:
		model = Friendship
		fields = ['receiver']

	def validate(self, attrs):
		request = self.context.get('request')
		receiver = attrs['receiver']
		if request.user == receiver:
			raise serializers.ValidationError("You cannot send a friend request to yourself.")
		if Friendship.objects.filter(requester=request.user, receiver=receiver).exists():
			raise serializers.ValidationError("Friend request already sent.")
		return attrs

	def create(self, validated_data):
		requester = self.context.get('request').user
		receiver = validated_data['receiver']
		friendship = Friendship.objects.create(requester=requester, receiver=receiver)
		return friendship
