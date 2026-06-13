import logging
import sys
# from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

import envs
from db.connect import engine
from db.tables import Base
from skills.admin import SkillsAdmin
from route.routers import user_router
from skills import managing, progress
import security
from middlwares.auth import AuthMiddleware

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

app = FastAPI()
app.include_router(user_router)
app.add_middleware(AuthMiddleware)

admin = Admin(app, engine)
admin.add_view(SkillsAdmin)





