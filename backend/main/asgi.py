"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .wsgi import *
from .middleware import JWTAuthMiddleware
from users import routing as userroute
from chat import routing as chatroute
from pong import routing as pongroute
from shooter import routing as shooterRoute

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = ProtocolTypeRouter({
	"http": get_asgi_application(),
	"websocket": JWTAuthMiddleware(
		URLRouter(
			userroute.websocket_urlpatterns +
			chatroute.websocket_urlpatterns +
			pongroute.websocket_urlpatterns +
			shooterRoute.websocket_urlpatterns
		)
	),
})
