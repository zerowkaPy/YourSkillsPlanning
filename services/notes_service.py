from typing import Annotated
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Header, Depends, Path

from db.connect import get_db
from middlwares.auth import get_user_id
from constants import BOT_ID
from repos.notes_repo import NotesRepo, NotesRepoBot


async def get_all_notes(
    session:AsyncSession,
    user_id:int|str,
    telegram_id:int|None):

    response = []
    if user_id == BOT_ID:
        notes = await NotesRepoBot.get_all_notes(session=session, telegram_id=telegram_id)
    else:
        notes = await NotesRepo.get_all_notes(session=session, user_id=user_id)
    
    for note, skill_name in notes:
        response.append({
            "skill":skill_name,
            "text":note.text,
            "created_at":note.created_at
        })
    return response


async def create_note(
    session:AsyncSession,
    skill_name:str,
    text:str,
    user_id:int|str,
    telegram_id:int|None):

    if user_id == BOT_ID:
        await NotesRepoBot.create_note(session=session, skill_name=skill_name, text=text, telegram_id=telegram_id)
    else:
        await NotesRepo.create_note(session=session, skill_name=skill_name, text=text, user_id=user_id)
    return "Note created"


async def delete_note(
    session:Annotated[AsyncSession, Depends(get_db)],
    skill_name:Annotated[str, Path()],
    created_at:datetime,
    user_id:Annotated[int|str, Depends(get_user_id)],
    telegram_id:Annotated[int|None, Header()] = None):

    if user_id == BOT_ID:
        await NotesRepoBot.delete_note(session=session, skill_name=skill_name, created_at=created_at, telegram_id=telegram_id)
    else:
        await NotesRepo.delete_note(session=session, skill_name=skill_name, created_at=created_at, user_id=user_id)
    return "Note deleted"


    