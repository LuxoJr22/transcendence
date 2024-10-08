import re
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.conf import settings
from rest_framework import serializers
from PIL import Image
from .models import User
import os
import shutil, sys

class ValidationMixin:
	def _validate_username(self, value):
		if value:
			if len(value) < 3:
				raise serializers.ValidationError("Username must be at least 3 characters long")
			if len(value) > 12:
				raise serializers.ValidationError("Username must not exceed 12 characters long")
			if not re.match("^[a-zA-Z0-9-._]+$", value):
				raise serializers.ValidationError("Username can only contain letters, numbers, hyphens, dots, and underscores.")
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

	def _validate_profile_picture(self, value):
		if value:
			try:
				image = Image.open(value)
			except Exception as e:
					raise serializers.ValidationError(f"Error processing image: {e}")
			if image.width > 1024 or image.height > 1024:
					raise serializers.ValidationError("Profile picture size cannot exceed 1024x1024 pixels")
		return value

class UserSerializer(ValidationMixin, serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'password', 'profile_picture']
		extra_kwargs = {
			'id': {'read_only':True},
			'password': {'write_only': True},
		}

	def validate_username(self, value):
		return self._validate_username(value)

	def validate_password(self, value):
		return self._validate_password(value)

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		user = User.objects.create_user(**validated_data, password=password)
		user.save()
		return user

class UserDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'profile_picture']
		extra_kwargs = {
			'id': {'read_only': True},
			'username': {'read_only': True},
			'email': {'read_only': True},
			'profile_picture': {'read_only': True},
		}

class UserUpdateSerializer(ValidationMixin, serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=False)
	current_password = serializers.CharField(write_only=True, required=False)

	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'current_password', 'profile_picture']
		extra_kwargs = {
			'username': {'required': False},
			'email': {'required': False},
			'password': {'write_only': True, 'required': False},
			'current_password': {'write_only': True, 'required': False},
		}

	def validate_username(self, value):
		return self._validate_username(value)

	def validate_password(self, value):
		return self._validate_password(value)

	def validate_profile_picture(self, value):
		validated_value = self._validate_profile_picture(value)
		print("Validating profile picture", file=sys.stderr)
		username = self.instance.username
		profile_pictures_path = os.path.join(settings.MEDIA_ROOT, f'profile_pictures/{username}')
		print(f"Profile pictures path: {profile_pictures_path}", file=sys.stderr)  # Debug
		if os.path.exists(profile_pictures_path):
			print(f"Removing profile pictures for {username}", file=sys.stderr)
			shutil.rmtree(profile_pictures_path)
		return validated_value

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
		validated_data.pop('current_password', None)
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		if 'password' in validated_data:
			instance.set_password(validated_data['password'])
		instance.save()
		return instance

class PublicUserSerializer(serializers.ModelSerializer):
	profile_picture_url = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ['id', 'username', 'profile_picture_url', 'is_online']

	def get_profile_picture_url(self, obj):
		if obj.profile_picture:
			return obj.profile_picture.url
		return None

class UserSkinSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['skin']
