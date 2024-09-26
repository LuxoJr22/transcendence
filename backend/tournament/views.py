from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Tournament
from .serializers import TournamentSerializer, JoinTournamentSerializer

class CreateTournamentView(generics.CreateAPIView):
	queryset = Tournament.objects.all()
	serializer_class = TournamentSerializer
	permission_classes = [IsAuthenticated]

class JoinTournamentView(generics.UpdateAPIView):
	serializer_class = JoinTournamentSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		tournament_id = self.kwargs['tournament_id']
		tournament = get_object_or_404(Tournament, id=tournament_id)
		return tournament
	
	def put(self, request, *args, **kwargs):
		tournament = self.get_object()

		if request.user in tournament.participants.all():
			return Response({'error': 'User already in tournament'}, status=status.HTTP_400_BAD_REQUEST)
		if tournament.is_full:
			return Response({'error': 'Tournament is full'}, status=status.HTTP_400_BAD_REQUEST)

		if tournament.participants.count() + 1 == 8:
			tournament.is_full = True
			tournament.save()


		serializer = self.get_serializer(tournament, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		return Response({'detail': 'User joined tournament'}, status=status.HTTP_200_OK)
