from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
	re_path(r'ws/pong/(?P<gamemode>.+)/(?P<room_name>.+)/$', consumers.PongConsumer.as_asgi()),
	re_path(r'ws/pong_matchmaking/(?P<gamemode>.+)/$', consumers.MatchmakingConsumer.as_asgi()),
	re_path(r'ws/pong_private_matchmaking/(?P<gamemode>.+)/(?P<game_id>.+)/$', consumers.PrivateMatchmakingConsumer.as_asgi()),
]
