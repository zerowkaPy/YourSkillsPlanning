from typing import Tuple
from datetime import datetime


from sqlalchemy import select, delete, and_
from sqlalchemy.engine.result import TupleResult
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import Note, Skill
from repos.users_repo import UsersRepoBot
from repos.skills_repo import SkillRepo


class NotesRepo:

    @classmethod
    async def get_all_notes(cls, *, session:AsyncSession, user_id:int|str) -> TupleResult[Tuple[Note, str]]:
        stmt = select(Note, Skill.name).join(Skill, Note.skill_id == Skill.id).where(Skill.user_id== user_id)
        notes = await session.execute(stmt)
        return notes.tuples()
    

    @classmethod
    async def create_note(cls, *, session:AsyncSession, skill_name:str, text:str, user_id:int|str):
        skill_id = SkillRepo.get_skill_id_by_name(skill_name=skill_name, user_id=user_id) # type: ignore
        stmt = insert(Note).values( skill_id=skill_id, text=text)
        await session.execute(stmt)
        await session.commit()
    

    @classmethod
    async def delete_note(cls, *, session:AsyncSession, skill_name:str, created_at:datetime, user_id:int|str):
        skill_id = SkillRepo.get_skill_id_by_name(skill_name=skill_name, user_id=user_id) # type: ignore
        stmt = delete(Note).where(
            and_(Note.skill_id == skill_id,
                 Note.created_at == created_at))
        await session.execute(stmt)
        await session.commit()


class NotesRepoBot:

    @classmethod
    async def get_all_notes(cls, *, session:AsyncSession, telegram_id:int|None) -> TupleResult[Tuple[Note, str]]:
        user_id = UsersRepoBot.user_id_subq(telegram_id=telegram_id)

        stmt = select(Note, Skill.name).join(Skill, Note.skill_id == Skill.id).where(Skill.user_id == user_id)
        notes = await session.execute(stmt)
        return notes.tuples()
    

    @classmethod
    async def create_note(cls, *, session:AsyncSession, skill_name:str, text:str, telegram_id:int|None):
        user_id = UsersRepoBot.user_id_subq(telegram_id=telegram_id)

        skill_id = SkillRepo.get_skill_id_by_name(skill_name=skill_name, user_id=user_id) # type: ignore
        stmt = insert(Note).values(skill_id=skill_id, text=text)
        await session.execute(stmt)
        await session.commit()

    
    @classmethod
    async def delete_note(cls, *, session:AsyncSession, skill_name:str, created_at:datetime, telegram_id:int|None):
        user_id = UsersRepoBot.user_id_subq(telegram_id=telegram_id)
        
        skill_id = SkillRepo.get_skill_id_by_name(skill_name=skill_name, user_id=user_id) # type: ignore
        stmt = delete(Note).where(
            and_(Note.skill_id == skill_id,
                 Note.created_at == created_at))
        await session.execute(stmt)
        await session.commit()