from typing import Tuple

from sqlalchemy import delete, ScalarSelect, select, Result, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import Progress, Skill
from repos.users_repo import UsersRepoBot
from repos.skills_repo import SkillRepo

class ProgressRepo:

    @classmethod
    async def create_skill(cls, *, session:AsyncSession, user_id:int|str, skill_id:int):
        stmt = insert(Progress).values(
            user_id=user_id,
            skill_id=skill_id
            )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def all_skills(cls, *, session:AsyncSession, user_id:int|str) -> Result[Tuple[Progress, str]]:
        stmt = select(Progress, Skill.name).join(Skill, Progress.skill_id == Skill.id
                                             ).where(Progress.user_id == user_id)
        global_progress = await session.execute(stmt)
        return global_progress


    @classmethod
    async def delete_skill(cls, *, session:AsyncSession, skill_id:ScalarSelect[int]):
        stmt = delete(Progress).where(Progress.skill_id == skill_id)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def add_to_progress(cls, *, session:AsyncSession, skill_name:str, user_id:int):
        skill_id = SkillRepo.get_skill_id_by_name(skill_name=skill_name, user_id=user_id)
        stmt = update(Progress).where(Progress.skill_id == skill_id).values(total_time = Progress.total_time + 1)
        await session.execute(stmt)
        await session.commit()


    @classmethod
    async def reduce_progress(cls, *, session:AsyncSession, skill_name:str, user_id:int):
        skill_id = SkillRepo.get_skill_id_by_name(skill_name=skill_name, user_id=user_id)
        stmt = update(Progress).where(Progress.skill_id == skill_id).values(total_time = Progress.total_time - 1)
        await session.execute(stmt)
        await session.commit()


    
class ProgressRepoBot:

    @classmethod
    async def all_skills(cls, *, session:AsyncSession, telegram_id:int|None) -> Result[Tuple[Progress, str]]:
        user_id = UsersRepoBot.user_id_subq(telegram_id=telegram_id)

        stmt = select(Progress, Skill.name).join(Skill, Progress.skill_id == Skill.id
                                             ).where(Progress.user_id == user_id)
        global_progress = await session.execute(stmt)
        return global_progress
    

    @classmethod
    async def add_to_progress(cls, *, session:AsyncSession, skill_name:str, telegram_id:int|None):
        user_id = UsersRepoBot.user_id_subq(telegram_id=telegram_id)
        skill_id = SkillRepo.get_skill_id_by_name(skill_name=skill_name, user_id=user_id)
        stmt = update(Progress).where(Progress.skill_id == skill_id).values(total_time = Progress.total_time + 1)
        await session.execute(stmt)
        await session.commit()


    @classmethod
    async def reduce_progress(cls, *, session:AsyncSession, skill_name:str, telegram_id:int|None):
        user_id = UsersRepoBot.user_id_subq(telegram_id=telegram_id)
        skill_id = SkillRepo.get_skill_id_by_name(skill_name=skill_name, user_id=user_id)
        stmt = update(Progress).where(Progress.skill_id == skill_id).values(total_time = Progress.total_time - 1)
        await session.execute(stmt)
        await session.commit()


