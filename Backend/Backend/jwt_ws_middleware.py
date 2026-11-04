# Backend/jwt_ws_middleware.py
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

@database_sync_to_async
def get_user(token):
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import AnonymousUser
    from rest_framework_simplejwt.tokens import AccessToken
    from rest_framework_simplejwt.exceptions import TokenError
    User = get_user_model()
    try:
        return User.objects.get(id=AccessToken(token)["user_id"])
    except (TokenError, KeyError, User.DoesNotExist):
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token = parse_qs(scope["query_string"].decode()).get("token", [None])[0]
        if token:
            scope["user"] = await get_user(token)
        return await super().__call__(scope, receive, send)