from typing import Any
from collections.abc  import Sequence
import logging

from sqlalchemy import select, delete, update, and_, ScalarSelect
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError

from src.db.tables.skill import SkillOrm
from src.models.skill import SkillBase
from src.enums.alchemy_exceptions import AlchemyExcs
from src.enums.repos_exceptions import ReposResults


logger = logging.getLogger(__name__)

class SkillRepo:

    @classmethod
    async def get_all_skills(cls, *, session: AsyncSession, user_id: int) -> Sequence[SkillOrm]:
        stmt = select(SkillOrm).where(SkillOrm.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().all()
    

    @classmethod
    async def get_skill_by_id(cls, *, session: AsyncSession, user_id: int, skill_id: int) -> SkillOrm | None:
        try:
            query = (select(SkillOrm)
                    .where(
                    and_(SkillOrm.user_id == user_id,
                        SkillOrm.id == skill_id)))
            result = await session.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as exc:
            await session.rollback()
            logger.exception(
        "Database error: %s",
        type(exc).__name__
            )


    @classmethod
    async def create_skill(cls, *, session:AsyncSession, skill: SkillBase, user_id:int|str) -> SkillOrm | AlchemyExcs:
        try:
            stmt = insert(SkillOrm).values(
                user_id=user_id,
                name=skill.name,
                desc=skill.desc,
                weight=skill.weight).returning(SkillOrm)
            
            result = await session.execute(stmt)
            returned_skill = result.scalar_one()
            await session.commit()
            return returned_skill
        except IntegrityError:
            await session.rollback()
            return AlchemyExcs.IntegrityErr
        except SQLAlchemyError as exc:
            await session.rollback()
            logger.exception(
        "Database error: %s",
        type(exc).__name__
            )
            return AlchemyExcs.GlobalErr
  

    @classmethod
    async def edit_skill(cls, *, session: AsyncSession, skill_id: int, user_id: int, values: dict[str, Any]):
        try:
            stmt = update(SkillOrm).where(
                and_(SkillOrm.id == skill_id),
                    SkillOrm.user_id == user_id).values(**values).returning(SkillOrm)
            result = await session.execute(stmt)
            await session.commit()
            updated_skill = result.scalar_one_or_none()
            if updated_skill is None:
                return ReposResults.NotUpdated
            return updated_skill
        
        except IntegrityError:
            await session.rollback()
            return AlchemyExcs.IntegrityErr
        except DataError:
            await session.rollback()
            return AlchemyExcs.DataErr
        except SQLAlchemyError as exc:
            await session.rollback()
            logger.exception(
        "Database error: %s",
        type(exc).__name__
            )
            return AlchemyExcs.GlobalErr


    @classmethod
    def get_skill_id_by_name(cls, *, skill_name: str, user_id: int | ScalarSelect[int]) -> ScalarSelect[int]:
        skill_id = select(SkillOrm.id).where(
                        and_(SkillOrm.name == skill_name),
                            SkillOrm.user_id == user_id).scalar_subquery()
        return skill_id


    @classmethod
    async def delete_skill(cls, *, session: AsyncSession, skill_id: int):
        try:
            stmt = delete(SkillOrm).where(SkillOrm.id == skill_id).returning(SkillOrm)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()
        except SQLAlchemyError as exc:
            await session.rollback()
            logger.exception(
        "Database error: %s",
        type(exc).__name__
            )
            return False


