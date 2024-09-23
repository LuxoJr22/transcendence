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
		user.profile_picture = 'profile_pictures/default.jpg'
		user.skin = 'default.glb'
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
	return f'profile_pictures/{instance.username}/{filename}'

class User(AbstractBaseUser):
	username = models.CharField(max_length=12, unique=True)
	email = models.EmailField(max_length=254, unique=True)
	profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True, null=True)
	skin = models.CharField(max_length=254, blank=True, null=True)

	is_active = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.username

	def save(self, *args, **kwargs):
		if self.pk:
			old_user = User.objects.get(pk=self.pk)

			if old_user.profile_picture and old_user.profile_picture != 'profile_pictures/default.jpg' and old_user.profile_picture != self.profile_picture:
				old_user.profile_picture.delete(save=False)

		super().save(*args, **kwargs)
