import logging
import sys


from fastapi import FastAPI

import constants
from route.routers import user_router
from middlwares.auth import AuthMiddleware
from handlers import skills_handlers, progress_handlers, graph_handlers
import authorization


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

app = FastAPI()
app.include_router(user_router)
app.add_middleware(AuthMiddleware)





