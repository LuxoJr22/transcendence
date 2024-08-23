import jwt
from django.conf import settings
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs

@database_sync_to_async
def get_user(token):
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
		user = get_user_model().objects.get(id=payload['user_id'])
		return user
	except Exception as e:
		return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
	async def __call__(self, scope, receive, send):
		query_string = parse_qs(scope["query_string"].decode())
		token = query_string.get("token", [None])[0]

		if (token):
			scope['user'] = await get_user(token)
		else:
			scope['user'] = AnonymousUser()

		return await super().__call__(scope, receive, send)
