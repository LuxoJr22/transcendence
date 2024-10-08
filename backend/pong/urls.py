from django.urls import path
from .views import PongMatchHistoryView, SkinsView

urlpatterns = [
	path('pong/skins/<int:game_id>/', SkinsView.as_view(), name='players_skin'),
	path('pong/history/<int:user_id>/', PongMatchHistoryView.as_view(), name='pong_match_history'),
]
