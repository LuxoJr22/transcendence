from django.urls import path
from .views import CreateTournamentView, JoinTournamentView

urlpatterns = [
	path('tournament/create/', CreateTournamentView.as_view(), name='create_tournament'),
	path('tournament/join/<int:tournament_id>/', JoinTournamentView.as_view(), name='join_tournament'),
]