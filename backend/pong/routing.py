from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
	re_path(r'ws/pong/(?P<gamemode>.+)/$', consumers.PongConsumer.as_asgi())
]