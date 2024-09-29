from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Tournament
from .serializers import TournamentSerializer

class CreateTournamentView(generics.CreateAPIView):
	queryset = Tournament.objects.all()
	serializer_class = TournamentSerializer
	permission_classes = [IsAuthenticated]
