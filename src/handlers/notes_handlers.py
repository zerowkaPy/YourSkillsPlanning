from typing import Annotated, Any
from fastapi import  Depends, Path, Body, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession


from src.tools.user_dependency import get_current_user
from src.tools.db_dependency import get_session
from src.services import notes_service


note_router = APIRouter()

@note_router.get("/notes/")
async def get_all_notes(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[dict[str, Any], Depends(get_current_user)]):
    
    return await notes_service.get_all_notes(session, user)

@note_router.post("/notes/{skill_id}", status_code=status.HTTP_201_CREATED)
async def create_note(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[dict[str, Any], Depends(get_current_user)],
    skill_id: Annotated[int, Path()],
    text: Annotated[str, Body()],):
    
    return await notes_service.create_note(session, skill_id, text)

@note_router.delete("/notes/{note_id}")
async def delete_note(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[dict[str, Any], Depends(get_current_user)],
    note_id: Annotated[int, Path()]):
    
    return await notes_service.delete_note(session, note_id)