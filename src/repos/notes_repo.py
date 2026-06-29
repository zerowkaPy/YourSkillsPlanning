from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.db.tables.note import NoteOrm, SkillOrm

class NotesRepo:

    @classmethod
    async def get_all_notes(cls, *, session: AsyncSession, user_id: int) -> Sequence[NoteOrm]:
        query = (
            select(NoteOrm)
            .join(SkillOrm, NoteOrm.skill_id == SkillOrm.id)
            .where(SkillOrm.user_id == user_id))
        result = await session.execute(query)
        notes =  result.scalars().all()
        return notes

    @classmethod
    async def create_note(cls, *, session: AsyncSession, skill_id: int, text: str):
        try:
            stmt = (insert(NoteOrm)
                    .values(skill_id=skill_id, text=text)
                    .returning(NoteOrm))
            result = await session.execute(stmt)
            await session.commit()
            note = result.scalar_one_or_none()
            return note
        except SQLAlchemyError:
            await session.rollback()
            return None


    @classmethod
    async def delete_note(cls, *, session:AsyncSession, note_id: int):
        try:
            stmt = (delete(NoteOrm)
                    .where(NoteOrm.id == note_id)
                    .returning(NoteOrm))
            result = await session.execute(stmt)
            await session.commit()
            note = result.scalar_one_or_none()
            return note
        except SQLAlchemyError:
            await session.rollback()
            return None
    
    @classmethod
    async def delete_all_notes(cls, *, session: AsyncSession, skill_id: int):
        try:
            stmt = delete(NoteOrm).where(NoteOrm.skill_id == skill_id)
            await session.execute(stmt)
            return True
        except SQLAlchemyError:
            await session.rollback()
            return False
