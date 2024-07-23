from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'password']
		extra_kwargs = {
			'id': {'read_only':True}
		}

	def create(self, data):
		password = data.pop('password', None)
		user = User.objects.create_user(**data, password=password)
		return user
