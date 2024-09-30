from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
	re_path(r'ws/tournament/(?P<gamemode>.+)/(?P<tournament_name>.+)/$', consumers.TournamentMatchmakingConsumer.as_asgi()),
]
