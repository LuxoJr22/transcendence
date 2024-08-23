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
		user.display_name = username
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_superuser(self, username, email, password=None):
		user =  self.create_user(username,email, password)
		user.is_superuser = True
		user.is_staff = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	username = models.CharField(max_length=12, unique=True)
	display_name = models.CharField(max_length=12, unique=False, blank=True)
	email = models.EmailField(max_length=254, unique=True)

	is_online = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.username
