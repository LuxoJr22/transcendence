import re
from django.contrib.auth.password_validation import validate_password as django_validate_password
from rest_framework import serializers
from .models import User

class ValidationMixin:
	def _validate_name(self, value, field_name):
		if len(value) < 3:
			raise serializers.ValidationError(f"{field_name} must be at least 3 characters long")
		if len(value) > 12:
			raise serializers.ValidationError(f"{field_name} must not exceed 12 characters long")
		if not re.match("^[a-zA-Z0-9-._]+$", value):
			raise serializers.ValidationError(f"{field_name} can only contain letters, numbers, hyphens, dots, and underscores.")
		return value
	
	def _validate_password(self, value):
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
			django_validate_password(value)
		return value

class UserSerializer(ValidationMixin, serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['id', 'username', 'display_name', 'email', 'password']
		extra_kwargs = {
			'id': {'read_only':True},
			'password': {'write_only': True},
		}

	def validate_username(self, value):
		return self._validate_name(value, field_name='Username')

	def validate_password(self, value):
		return self._validate_password(value)

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		user = User.objects.create_user(**validated_data, password=password)
		return user

class UserUpdateSerializer(ValidationMixin, serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=False)
	current_password = serializers.CharField(write_only=True, required=False)

	class Meta:
		model = User
		fields = ['username', 'display_name', 'email', 'password', 'current_password']
		extra_kwargs = {
			'username': {'required': False},
			'email': {'required': False},
			'password': {'write_only': True, 'required': False},
			'current_password': {'write_only': True, 'required': False},
			'display_name': {'required': False},
		}

	def validate_username(self, value):
		return self._validate_name(value, field_name='Username')

	def validate_display_name(self, value):
		return self._validate_name(value, field_name='Display name')

	def validate_password(self, value):
		return self._validate_password(value)

	def validate(self, attrs):
		if 'password' in attrs:
			current_password = attrs.get('current_password')
			if not current_password:
				raise serializers.ValidationError({'current_password': ["Current password is required to set a new password"]})
			user = self.instance
			if not user.check_password(current_password):
				raise serializers.ValidationError({'current_password': ["Current password is incorrect"]})
		return attrs

	def update(self, instance, validated_data):
		password = validated_data.pop('password', None)
		validated_data.pop('current_password', None)
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		if password:
			instance.set_password(password)
		instance.save()
		return instance
