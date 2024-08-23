from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from .serializers import UserSerializer

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
				"display_name": user.display_name,
				"email": user.email,
			}
		})
