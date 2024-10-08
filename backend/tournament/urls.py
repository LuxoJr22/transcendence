from django.urls import path
from .views import CreateTournamentView, TournamentListView

urlpatterns = [
	path('tournament/create/', CreateTournamentView.as_view(), name='create_tournament'),
	path('tournament/list/', TournamentListView.as_view(), name='user_list'),
]
