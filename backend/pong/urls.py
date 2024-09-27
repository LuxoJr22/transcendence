from django.urls import path
from .views import PongMatchHistoryView, OponentSkinView

urlpatterns = [
	path('pong/skins/<int:game_id>', OponentSkinView.as_view(), name='oponent_skin'),
	path('pong/history/', PongMatchHistoryView.as_view(), name='pong_match_history'),
]