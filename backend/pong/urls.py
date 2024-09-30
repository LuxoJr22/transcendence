from django.urls import path
from .views import PongMatchHistoryView, SkinsView

urlpatterns = [
	path('pong/skins/<int:game_id>', SkinsView.as_view(), name='oponent_skin'),
	path('pong/history/', PongMatchHistoryView.as_view(), name='pong_match_history'),
]