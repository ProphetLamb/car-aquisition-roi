from starlette.applications import Starlette
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser
)
from starlette.routing import Route
from starlette.responses import PlainTextResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
import uvicorn
import logging
from dotenv import load_dotenv
import os
import base64

from api import api_routes

load_dotenv()
client_id = os.getenv('CAR_CLIENT_ID')
assert client_id, "A shared client id between the server and client is required"
debug = os.getenv('DEBUG', False)
origin = os.getenv('ORIGIN', 'http://127.0.0.1:3000').split(',')
host = origin[0].split('//')[1]
host, port = host.split(':')
port = int(port) if port else None
assert port, "A port must be specified in the ORIGIN environment variable"

logging.basicConfig(level=logging.INFO if debug else logging.WARNING)

class ClientIdBearerTokenBackend(AuthenticationBackend):
    async def validate_token(token: str) -> bool:
        return token == client_id

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

app = Starlette(
    debug=debug,
    routes=api_routes, 
    middleware=[
        Middleware(CORSMiddleware, allow_origins=origin, allow_methods=['*'], allow_headers=['*']),
        Middleware(AuthenticationMiddleware, backend=ClientIdBearerTokenBackend())
    ]
)

if __name__ == "__main__":
    logging.info(f"Starting server on {host}:{port}")
    uvicorn.run("server:app", reload=True, port=port, host=host, log_level="info" if debug else "warning")