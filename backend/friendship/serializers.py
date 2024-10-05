from rest_framework import serializers
from .models import Friendship, Block
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
		if Friendship.objects.filter(receiver=request.user, requester=receiver).exists():
			raise serializers.ValidationError("This user has already sent you a friend request.")
		if Block.objects.filter(blocker=request.user, blocked=receiver).exists():
			raise serializers.ValidationError("You have blocked this user.")
		if Block.objects.filter(blocker=receiver, blocked=request.user).exists():
			raise serializers.ValidationError("This user has blocked you.")
		return attrs

	def create(self, validated_data):
		requester = self.context.get('request').user
		receiver = validated_data['receiver']
		friendship = Friendship.objects.create(requester=requester, receiver=receiver)
		return friendship

class BlockSerializer(serializers.ModelSerializer):
	blocker = PublicUserSerializer(read_only=True)
	blocked = PublicUserSerializer(read_only=True)

	class Meta:
		model = Block
		fields = ['id', 'blocker', 'blocked', 'created_at']

class CreateBlockSerializer(serializers.ModelSerializer):
	class Meta:
		model = Block
		fields = ['blocked']

	def validate(self, attrs):
		request = self.context.get('request')
		blocked = attrs['blocked']
		if request.user == blocked:
			raise serializers.ValidationError("You cannot block yourself.")
		if Block.objects.filter(blocker=request.user, blocked=blocked).exists():
			raise serializers.ValidationError("You have already blocked this user.")
		return attrs

	def create(self, validated_data):
		blocker = self.context.get('request').user
		blocked = validated_data['blocked']
		block = Block.objects.create(blocker=blocker, blocked=blocked)
		return block
