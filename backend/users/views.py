from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import TriplumUser
from .serializers import TriplumUserSerializer

class TriplumRegisterView(generics.CreateAPIView):
	queryset = TriplumUser.objects.all()
	serializer_class = TriplumUserSerializer
	permission_classes = [AllowAny] # Access to this view
