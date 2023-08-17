#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
import uvicorn
import logging
from auth import ClientIdBearerTokenBackend

import router
import cfg

cfg.load()

logging.basicConfig(level=logging.INFO if cfg.debug else logging.WARNING)

app = Starlette(
    debug=cfg.debug,
    routes=[router.api_routes],
    middleware=[
        Middleware(CORSMiddleware, allow_origins=cfg.origin, allow_methods=['*'], allow_headers=['*']),
        Middleware(AuthenticationMiddleware, backend=ClientIdBearerTokenBackend())
    ]
)

if __name__ == "__main__":
    logging.info(f"Starting server on {cfg.host}:{cfg.port}")
    uvicorn.run("server:app", reload=True, port=cfg.port, host=cfg.host, log_level="info" if cfg.debug else "warning")
