from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Tournament
from .serializers import TournamentSerializer, TournamentListSerializer

class CreateTournamentView(generics.CreateAPIView):
	queryset = Tournament.objects.all()
	serializer_class = TournamentSerializer
	permission_classes = [IsAuthenticated]

class TournamentListView(generics.ListAPIView):
	queryset = Tournament.objects.all()
	serializer_class = TournamentListSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Tournament.objects.all()
