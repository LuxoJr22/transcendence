from rest_framework import serializers
from .models import TriplumUser

class TriplumUserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = TriplumUser
		fields = ['id', 'username', 'email', 'password']
		extra_kwargs = {
			'id': {'read_only':True}
		}

	def create(self, data):
		password = data.pop('password', None)
		user = TriplumUser.objects.create_user(**data, password=password)
		return user
