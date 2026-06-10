import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

import envs
from db.sync_engine import engine
from db.tables import Base
from skills.admin import SkillsAdmin
from skills.managing import skill_router


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

app = FastAPI(lifespan=lifespan)
app.include_router(skill_router)

admin = Admin(app, engine)
admin.add_view(SkillsAdmin)





