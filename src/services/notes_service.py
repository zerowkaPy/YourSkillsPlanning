from typing import Annotated, Any

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.repos.notes_repo import NotesRepo
from src.models.note import NoteResponse
from src.errors_handling.funcs import throw_404
from src.tools.user_dependency import get_current_user
from src.tools.db_dependency import get_session


async def get_all_notes(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[dict[str, Any], Depends(get_current_user)]):

    user_id = user["user_id"]
    notes = await NotesRepo.get_all_notes(session=session, user_id=user_id)
    if not notes:
        return {"notes" : []}
    notes_list = [NoteResponse.model_validate(note) for note in notes]
    return {"notes" : notes_list}

async def create_note(
    session: Annotated[AsyncSession, Depends(get_session)],
    skill_id: int,
    text: str):

    note = await NotesRepo.create_note(session=session, skill_id=skill_id, text=text)
    
    if note is None:
        raise throw_404(f"Skill with id {skill_id} wasn't found")
    return NoteResponse.model_validate(note)


async def delete_note(
    session: Annotated[AsyncSession, Depends(get_session)],
    note_id: int):

    note = await NotesRepo.delete_note(session=session,note_id=note_id)
    if note is None:
        raise throw_404(f"Note with id {note_id} wasn't found")
    return NoteResponse.model_validate(note)


    