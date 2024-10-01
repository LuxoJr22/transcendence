import os, requests
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.views.generic import RedirectView
from .models import User
from .serializers import UserSerializer, UserUpdateSerializer, PublicUserSerializer, UserGameDataSerializer, UserSkinSerializer

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
	serializer_class = UserSerializer
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
		}, status=status.HTTP_200_OK)

class UserUpdateView(generics.UpdateAPIView):
	serializer_class = UserUpdateSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user

class UserProfileView(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = PublicUserSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		user_id = self.kwargs['id']
		user = generics.get_object_or_404(User, id=user_id)
		return user

class UserGameDataView(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserGameDataSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user

class UserSkinUpdateView(generics.UpdateAPIView):
	serializer_class = UserSkinSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user

# class OAuth42RedirectView(RedirectView):
# 	def get_redirect_url(self, *args, **kwargs):
# 		CLIENT_ID = os.environ.get('CLIENT_ID')
# 		REDIRECT_URI = os.environ.get('REDIRECT_URI')
# 		return f'https://api.intra.42.fr/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code'

# class OAuth42CallbackView(generics.CreateAPIView):
# 	permission_classes = [AllowAny]

# 	def post(self, request):
# 		code = request.data['code']

# 		CLIENT_ID = os.environ.get('CLIENT_ID')
# 		CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
# 		REDIRECT_URI = os.environ.get('REDIRECT_URI')

# 		response = requests.post('https://api.intra.42.fr/oauth/token', data={
# 			'grant_type': 'authorization_code',
# 			'client_id': CLIENT_ID,
# 			'client_secret': CLIENT_SECRET,
# 			'code': code,
# 			'redirect_uri': REDIRECT_URI,
# 		})
# 		return Response(response.json())
