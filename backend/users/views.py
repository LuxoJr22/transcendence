from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import TriplumUser
from .serializers import TriplumUserSerializer

class TriplumRegisterView(generics.CreateAPIView):
	queryset = TriplumUser.objects.all()
	serializer_class = TriplumUserSerializer
	permission_classes = [AllowAny] # Access to this view

class TriplumUserDetailView(APIView):
	permission_classes = [IsAuthenticated]
	
	def get(self, request):
		user = request.user
		data = {
			'id': user.id,
			'username': user.username,
			'email': user.email,
		}
		return Response(data)
