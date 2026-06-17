from typing import Annotated
from datetime import datetime
from fastapi import Header, Depends, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession

from route.routers import user_router
from db.connect import get_db
from middlwares.auth import get_user_id
from services import notes_service


@user_router.get("/notes/")
async def get_all_notes(
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):
    
    return await notes_service.get_all_notes(session, user_id, telegram_id)



@user_router.post("/notes/{skill_name}")
async def create_note(
        session:Annotated[AsyncSession, Depends(get_db)],
        skill_name:Annotated[str, Path()],
        text:Annotated[str, Body()],
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):
    
    return await notes_service.create_note(session, skill_name, text, user_id, telegram_id)


@user_router.delete("/notes/{skill_name}")
async def delete_note(
    session:Annotated[AsyncSession, Depends(get_db)],
        skill_name:Annotated[str, Path()],
        created_at:Annotated[datetime, Body()],
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):
    
    return await notes_service.delete_note(session, skill_name, created_at, user_id, telegram_id)