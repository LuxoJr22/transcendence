from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		if not username:
			raise ValueError('The username must be set')
		if not email:
			raise ValueError('The email must be set')
		if not password:
			raise ValueError('The password must be set')
		email = self.normalize_email(email)
		user = self.model(username=username, email=email)
		user.settings = Settings.objects.create()
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password=None):
		user =  self.create_user(username,email, password)
		user.is_superuser = True
		user.is_staff = True
		user.save(using=self._db)
		return user

def user_profile_picture_path(instance, filename):
	return f'profile_pictures/{instance.id}/{filename}'

def pong_dict():
	return {"up":87 , "down": 83, "left":65, "right":68, "charge":32}

def shooter_dict():
	return {"up": 87, "down": 83, "left":65, "right":68, "jump":32}

class Settings(models.Model):
	pong = models.JSONField(default=pong_dict)
	shooter = models.JSONField(default=shooter_dict)

class User(AbstractBaseUser):
	username = models.CharField(max_length=12, unique=True)
	email = models.EmailField(max_length=254, unique=True)
	login42 = models.CharField(max_length=8, unique=True, blank=True, null=True, default=None)

	profile_picture = models.ImageField(upload_to=user_profile_picture_path, default='profile_pictures/default.jpg')
	skin = models.CharField(max_length=254, default='default.glb')
	pong_elo = models.IntegerField(default=600)
	shooter_elo = models.IntegerField(default=600)
	settings = models.ForeignKey(Settings,  on_delete=models.CASCADE)

	is_online = models.BooleanField(default=False)

	is_active = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	is_2fa_enabled = models.BooleanField(default=False)
	otp_secret = models.CharField(max_length=32, blank=True, null=True, default=None)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.username

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

	def has_perm(self, perm, obj=None):
		return self.is_superuser

	def has_module_perms(self, app_label):
		return self.is_superuser
