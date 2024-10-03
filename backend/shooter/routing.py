from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
	re_path(r'ws/shooter/(?P<room_name>.+)/$', consumers.ShooterConsumer.as_asgi())
]