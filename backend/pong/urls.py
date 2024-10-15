from django.urls import path
from .views import PongMatchView, PongMatchHistoryView, SkinsView, PongSettingsView

urlpatterns = [
	path('pong/match/<int:match_id>/', PongMatchView.as_view(), name='pong_match'),
	path('pong/history/<int:user_id>/', PongMatchHistoryView.as_view(), name='pong_match_history'),
	path('pong/skins/<int:game_id>/', SkinsView.as_view(), name='players_skin'),
	path('pong/settings/<int:user_id>/', PongSettingsView.as_view(), name='players_settings'),
]
