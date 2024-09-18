from django.urls import path
from . import consumers

websocket_urlpatterns = [
	path('ws/shooter/', consumers.ShooterConsumer.as_asgi())
]