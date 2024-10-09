from django.urls import path
from .views import PongMatchHistoryView, SkinsView, SettingsView

urlpatterns = [
	path('pong/skins/<int:game_id>/', SkinsView.as_view(), name='players_skin'),
	path('pong/settings/<int:user_id>/', SettingsView.as_view(), name='players_settings'),
	path('pong/history/<int:user_id>/', PongMatchHistoryView.as_view(), name='pong_match_history'),
]
