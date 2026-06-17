from typing import Annotated

from fastapi import Depends, Path, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession

from db.connect import get_db
from route.routers import user_router
from middlwares.auth import get_user_id
from services import progress_service

@user_router.get("/progress/")
async def global_progress(
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):
    
    return await progress_service.global_progress(session, user_id, telegram_id)
    

@user_router.patch("/progress/{skill_name}")
async def edit_progress(
    session:Annotated[AsyncSession, Depends(get_db)],
    user_id:Annotated[int|str, Depends(get_user_id)],
    skill_name:Annotated[str, Path(max_length=35)],
    telegram_id:Annotated[int|None, Header()] = None,
    reduce:Annotated[bool, Query()] = False,
    add:Annotated[bool, Query()] = False
    ):

    return await progress_service.edit_progress(session, user_id, skill_name, telegram_id, reduce, add)

