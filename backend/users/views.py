import os, requests, pyotp, qrcode, base64
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import models
from django.views.generic import RedirectView
from django.core.exceptions import ValidationError
from io import BytesIO
from friendship.models import Block
from .models import User, Settings
from .serializers import UserSerializer, UserUpdateSerializer, UserDetailSerializer, PublicUserSerializer, UserSkinSerializer

class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [AllowAny]

class LoginView(TokenObtainPairView):
	serializer_class = TokenObtainPairSerializer
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		user = User.objects.get(username=request.data['username'])

		if user.is_2fa_enabled:
			return Response({'is_2fa_enabled': True}, status=status.HTTP_200_OK)

		refresh = RefreshToken.for_user(user)
		return Response({
			"refresh": str(refresh),
			"access": str(refresh.access_token),
			"user": {
				"id": user.id,
				"username": user.username,
				"email": user.email,
				"profile_picture_url": user.profile_picture.url,
			}
		}, status=status.HTTP_200_OK)

class UserDetailView(generics.RetrieveAPIView):
	serializer_class = UserDetailSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user

	def get(self, request):
		user = self.get_object()
		return Response({
			"id": user.id,
			"username": user.username,
			"email": user.email,
			"profile_picture": user.profile_picture.url,
			"skin": user.skin,
			"is_2fa_enabled": user.is_2fa_enabled,
		}, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = PublicUserSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		user_id = self.kwargs['id']
		user = generics.get_object_or_404(User, id=user_id)
		return user

class UserListView(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = PublicUserSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user

		blocked_users = Block.objects.filter(models.Q(blocker=user) | models.Q(blocked=user)).values_list('blocker', 'blocked')
		blocked_user_ids = set()
		for blocker, blocked in blocked_users:
			if blocker == user.id:
				blocked_user_ids.add(blocked)
			else:
				blocked_user_ids.add(blocker)

		return User.objects.exclude(id__in=blocked_user_ids).exclude(id=user.id)

class UserUpdateView(generics.UpdateAPIView):
	serializer_class = UserUpdateSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user

class UserSkinUpdateView(generics.UpdateAPIView):
	serializer_class = UserSkinSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user
	
class SettingsUpdateView(generics.UpdateAPIView):
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user.settings
	
	def patch(self, request):
		pong_keys = ["up", "down", "left", "right", "charge"]
		shooter_keys = ["up", "down", "left", "right", "jump"]
		settings = self.get_object()
		shooter_dict = request.data['shooter']
		pong_dict = request.data['pong']
		for key in shooter_keys:
			try:
				value = shooter_dict[key]
			except:
				raise ValidationError("keys are not valid")
		for key in pong_keys:
			try:
				value = pong_dict[key]
			except:
				raise ValidationError("keys are not valid")
		settings.shooter = request.data['shooter']
		settings.pong = request.data['pong']
		settings.save()

		return Response({'success': 'Key changed'}, status=status.HTTP_200_OK)


class OAuth42RedirectView(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		CLIENT_ID = os.environ.get('CLIENT_ID')
		REDIRECT_URI = os.environ.get('REDIRECT_URI')
		return f'https://api.intra.42.fr/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code'

class OAuth42CallbackView(generics.CreateAPIView):
	permission_classes = [AllowAny]

	def find_or_create_42user(self, user_info):
		if User.objects.filter(login42=user_info['login']).exists():
			return User.objects.get(login42=user_info['login'])
		
		username = user_info['login']
		i = 0
		while User.objects.filter(username=username).exists():
			i += 1
			username = f"{user_info['login']}{str(i)}"
		if len(username) > 12:
			raise ValidationError("Triplum internal error, please create regular account.")

		if User.objects.filter(email=user_info['email']).exists():
			raise ValidationError("An account with this email already exists")

		user = User.objects.create(
			username=username,
			email=user_info['email'],
			login42=user_info['login'],
			password='42_OAuth',
			settings = Settings.objects.create(),
		)
		user.save()
		return user

	def post(self, request):
		code = request.data['code']

		if code is None:
			return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)

		CLIENT_ID = os.environ.get('CLIENT_ID')
		CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
		REDIRECT_URI = os.environ.get('REDIRECT_URI')

		response = requests.post(
			'https://api.intra.42.fr/oauth/token', 
			data={
				'grant_type': 'authorization_code',
				'code': code,
				'client_id': CLIENT_ID,
				'client_secret': CLIENT_SECRET,
				'redirect_uri': REDIRECT_URI,
		})

		if response.status_code != 200:
			return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
		
		access_token = response.json()['access_token']
		user_info_response = requests.get(
			'https://api.intra.42.fr/v2/me',
			headers={
				'Authorization': f'Bearer {access_token}'
			})
		
		if user_info_response.status_code != 200:
			return Response({'error': 'Invalid access token'}, status=status.HTTP_400_BAD_REQUEST)
		
		user_info = user_info_response.json()
		try:
			user = self.find_or_create_42user(user_info)
		except ValidationError as e:
			return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

		if user is None:
			return Response({'error': 'Triplum internal error, please create regular account'}, status=status.HTTP_400_BAD_REQUEST)
		
		refresh = RefreshToken.for_user(user)
		return Response({
			"refresh": str(refresh),
			"access": str(refresh.access_token),
			"user": {
				"id": user.id,
				"username": user.username,
				"email": user.email,
				"profile_picture_url": user.profile_picture.url,
			}
		}, status=status.HTTP_200_OK)

class QRCode2FAView(generics.GenericAPIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		user = request.user
		
		if user.is_2fa_enabled:
			return Response({'error': '2FA is already enabled'}, status=status.HTTP_400_BAD_REQUEST)

		user.otp_secret = pyotp.random_base32()
		user.save()

		otp_uri = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(user.username, issuer_name='Triplum')

		img = qrcode.make(otp_uri)
		buf = BytesIO()
		img.save(buf, format='PNG')
		buf.seek(0)

		qr_code_base64 = base64.b64encode(buf.read()).decode('utf-8')

		return Response({
			'otp_secret': user.otp_secret,
			'qr_code': qr_code_base64
		}, status=status.HTTP_200_OK)

class Enable2FAView(generics.GenericAPIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		user = request.user

		if not 'otp_code' in request.data:
			return Response({'error': 'No 2FA code provided'}, status=status.HTTP_400_BAD_REQUEST)

		totp = pyotp.TOTP(user.otp_secret)
		if not totp.verify(request.data['otp_code']):
			return Response({'error': 'Invalid 2FA code'}, status=status.HTTP_400_BAD_REQUEST)

		user.is_2fa_enabled = True
		user.save()

		return Response({'success': '2FA is enabled'}, status=status.HTTP_200_OK)

class Disable2FAView(generics.GenericAPIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		user = request.user

		if not user.is_2fa_enabled:
			return Response({'error': '2FA is not enabled'}, status=status.HTTP_400_BAD_REQUEST)

		if not 'otp_code' in request.data:
			return Response({'error': 'No 2FA code provided'}, status=status.HTTP_400_BAD_REQUEST)

		totp = pyotp.TOTP(user.otp_secret)
		if not totp.verify(request.data['otp_code']):
			return Response({'error': 'Invalid 2FA code'}, status=status.HTTP_400_BAD_REQUEST)

		user.is_2fa_enabled = False
		user.otp_secret = None
		user.save()

		return Response({'success': '2FA is disabled'}, status=status.HTTP_200_OK)

class Verify2FAView(TokenObtainPairView):
	serializer_class = TokenObtainPairSerializer

	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		user = User.objects.get(username=request.data['username'])

		if not 'otp_code' in request.data:
			return Response({'error': 'No 2FA code provided'}, status=status.HTTP_400_BAD_REQUEST)

		totp = pyotp.TOTP(user.otp_secret)
		if not totp.verify(request.data['otp_code']):
			return Response({'error': 'Invalid 2FA code'}, status=status.HTTP_400_BAD_REQUEST)

		refresh = RefreshToken.for_user(user)
		return Response({
			"refresh": str(refresh),
			"access": str(refresh.access_token),
			"user": {
				"id": user.id,
				"username": user.username,
				"email": user.email,
				"profile_picture_url": user.profile_picture.url,
			}
		}, status=status.HTTP_200_OK)
