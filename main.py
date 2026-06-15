import logging
import sys


from fastapi import FastAPI
from sqladmin import Admin

import envs
from db.connect import engine
from db.tables import Base
from skills.admin import SkillsAdmin
from route.routers import user_router
from middlwares.auth import AuthMiddleware
from skills import managing, progress
import authorization


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

app = FastAPI()
app.include_router(user_router)
app.add_middleware(AuthMiddleware)

admin = Admin(app, engine)
admin.add_view(SkillsAdmin)





