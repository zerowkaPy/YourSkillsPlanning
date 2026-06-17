from typing import Any
from collections.abc  import Sequence

from sqlalchemy import Result, select, delete, update, and_, ScalarSelect
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import Skill
from models.skill import SkillModel
from repos.users_repo import UsersRepoBot


class SkillRepo:

    @classmethod
    async def get_all_skills(cls, *, session:AsyncSession, user_id:int|str) -> Sequence[Skill]:
        stmt = select(Skill).where(Skill.user_id == user_id)
        result:Result[tuple[Skill]] = await session.execute(stmt)
        return result.scalars().all()
    
    
    @classmethod
    async def create_skill(cls, *, session:AsyncSession, skill:SkillModel, user_id:int|str) -> int:
        stmt = insert(Skill).values(
            user_id=user_id,
            name=skill.name,
            desc=skill.desc,
            weight=skill.weight).returning(Skill.id)
        
        result = await session.execute(stmt)
        await session.commit()
        skill_id = result.scalar_one()
        return skill_id

  

    @classmethod
    async def edit_skill(cls, *, session:AsyncSession, skill_name:str, user_id:int|str, values:dict[str, Any]):
        stmt = update(Skill).where(
            and_(Skill.name == skill_name),
                Skill.user_id == user_id).values(**values)
        await session.execute(stmt)
        await session.commit()


    @classmethod
    def get_skill_id_by_name(cls, *, skill_name:str, user_id:int|ScalarSelect[int]) -> ScalarSelect[int]:
        skill_id = select(Skill.id).where(
                        and_(Skill.name == skill_name),
                            Skill.user_id == user_id).scalar_subquery()
        return skill_id


    @classmethod
    async def delete_skill(cls, *, session:AsyncSession, skill_id:ScalarSelect[int]):
        stmt = delete(Skill).where(Skill.id == skill_id)
        await session.execute(stmt)
        await session.commit()



class SkillRepoBot:

    @classmethod
    async def get_all_skills(cls, *, session:AsyncSession, telegram_id:int|None) -> Sequence[Skill]:
        user_id = UsersRepoBot.user_id_subq(telegram_id=telegram_id)

        stmt = select(Skill).where(Skill.user_id == user_id)
        result:Result[tuple[Skill]] = await session.execute(stmt)
        return result.scalars().all()
    

    @classmethod
    async def create_skill(cls, *, session:AsyncSession, skill:SkillModel, telegram_id:int|None) -> int:
        user_id = UsersRepoBot.user_id_subq(telegram_id=telegram_id)

        skill_stmt = insert(Skill).values(
            user_id=user_id,
            name=skill.name,
            desc=skill.desc,
            weight=skill.weight).returning(Skill.id)
        
        result = await session.execute(skill_stmt)
        await session.commit()
        skill_id = result.scalar_one()
        return skill_id


    @classmethod
    async def edit_skill(cls, *, session:AsyncSession, skill_name:str, telegram_id:int|None, values:dict[str, Any]):
        user_id = UsersRepoBot.user_id_subq(telegram_id=telegram_id)
      
        stmt = update(Skill).where(
            and_(Skill.name == skill_name),
                Skill.user_id == user_id).values(**values)
        await session.execute(stmt)
        await session.commit()
       

    @classmethod
    def get_skill_id_by_name(cls, *, skill_name:str, telegram_id:int|None) -> ScalarSelect[int]:
        user_id = UsersRepoBot.user_id_subq(telegram_id=telegram_id)

        skill_id = select(Skill.id).where(
            and_(Skill.name == skill_name,
                Skill.user_id == user_id)).scalar_subquery()
        return skill_id
    
