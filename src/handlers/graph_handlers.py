from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connect import get_db
from src.route.routers import user_router
from src.middlwares.auth import get_user_id

from src.services import  graph_service


@user_router.get("/skills/graph")
async def make_graph(
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):
    
    return await graph_service.make_graph(session, user_id, telegram_id)

