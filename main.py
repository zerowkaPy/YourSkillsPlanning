import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

import envs
from db.connect import engine
from db.tables import Base
from skills.admin import SkillsAdmin
from route.routers import user_router
from skills import managing, progress


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)

admin = Admin(app, engine)
admin.add_view(SkillsAdmin)





