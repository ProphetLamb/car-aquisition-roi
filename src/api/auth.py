from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser
)
import base64

import cfg

class ClientIdBearerTokenBackend(AuthenticationBackend):
    async def validate_token(self, token: str) -> bool:
        return token == cfg.client_id

    async def authenticate(self, conn):
        authorization = conn.headers['Authorization']
        try:
            method, token = authorization.split(' ')
            if method != 'Bearer':
                return
            token = base64.b64decode(token).decode('utf-8')
        except Exception as error:
            raise AuthenticationError('Invalid Authorization header')
        if not await self.validate_token(token):
            raise AuthenticationError('Invalid bearer token')
        return AuthCredentials(["authenticated"]), SimpleUser(token)
