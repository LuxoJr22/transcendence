import re
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

	def validate_username(self, value):
		if len(value) < 3:
			raise serializers.ValidationError("Username must be at least 3 characters long")
		if len(value) > 12:
			raise serializers.ValidationError("Username must not exceed 12 characters long")
		if not re.match("^[a-zA-Z0-9-._]+$", value):
			raise serializers.ValidationError("The username can only contain letters, numbers, hyphens, dots and underscores.")
		return value

	def validate_password(self, value):
		if value:
			if len(value) < 8:
				raise serializers.ValidationError("Password must be at least 8 characters long")
			if len(value) > 32:
				raise serializers.ValidationError("Password must not exceed 32 characters long")
			if not re.search("[A-Z]", value):
				raise serializers.ValidationError("Password must contain at least one capital letter")
			if not re.search("[a-z]", value):
				raise serializers.ValidationError("Password must contain at least one lowercase letter")
			if not re.search("[0-9]", value):
				raise serializers.ValidationError("Password must contain at least one digit")
			if not re.search("[!@#$%^&*()_+=-]", value):
				raise serializers.ValidationError("Password must contain at least one special character")
		return value

	def create(self, data):
		password = data.pop('password', None)
		user = User.objects.create_user(**data, password=password)
		return user
