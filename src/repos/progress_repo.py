from typing import Any, Sequence
import logging

from sqlalchemy import delete, select, update, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.db.tables.progress import ProgressOrm
from src.enums.repos_exceptions import ReposResults

logger = logging.getLogger(__name__)


class ProgressRepo:

    @classmethod
    async def create_progress(cls, *, session: AsyncSession, user_id: int, skill_id: int):
        try:
            stmt = insert(ProgressOrm).values(
                user_id=user_id,
                skill_id=skill_id
                )
            await session.execute(stmt)
            await session.commit()
        except SQLAlchemyError as exc:
            await session.rollback()
            logger.exception(
        "Database error: %s",
        type(exc).__name__
            )     


    @classmethod
    async def all_progress(cls, *, session: AsyncSession, user_id: int | Any) -> Sequence[ProgressOrm]:
        query = select(ProgressOrm).where(ProgressOrm.user_id == user_id)
        progress = await session.execute(query)
        return progress.scalars().all()


    @classmethod
    async def delete_progress(cls, *, session: AsyncSession, skill_id: int):
        try:
            stmt = delete(ProgressOrm).where(ProgressOrm.skill_id == skill_id)
            await session.execute(stmt)
            await session.commit()
            return True
        except SQLAlchemyError:
            await session.rollback()
            return False
        

    @classmethod
    async def add_to_progress(cls, *, session: AsyncSession, skill_id: int, user_id: int):
        try:
            stmt = (update(ProgressOrm)
                    .where(
                        and_(ProgressOrm.skill_id == skill_id,
                             ProgressOrm.user_id == user_id))
                    .values(total_time=ProgressOrm.total_time + 1)
                    .returning(ProgressOrm))
            returned = await session.execute(stmt)
            progress = returned.scalar_one_or_none()
            if progress is None:
                return ReposResults.NotUpdated
            await session.commit()
            return progress
        
        except SQLAlchemyError:
            await session.rollback()
            return ReposResults.NotUpdated

    @classmethod
    async def reduce_progress(cls, *, session: AsyncSession, skill_id: int, user_id: int):
        try:
            stmt = (update(ProgressOrm)
                    .where(
                        and_(ProgressOrm.skill_id == skill_id,
                             ProgressOrm.user_id == user_id))
                    .values(total_time=ProgressOrm.total_time - 1)
                    .returning(ProgressOrm))
            returned = await session.execute(stmt)
            progress = returned.scalar_one_or_none()
            if progress is None:
                return ReposResults.NotUpdated
            await session.commit()
            return progress
        
        except SQLAlchemyError:
            await session.rollback()
            return ReposResults.NotUpdated

    @classmethod
    async def get_one_progress(cls, *, session: AsyncSession, skill_id: int, user_id: int):
        query = (select(ProgressOrm)
                 .where(
                     and_(ProgressOrm.skill_id == skill_id,
                          ProgressOrm.user_id == user_id)))
        result = await session.execute(query)
        progress = result.scalar_one_or_none()
        if progress is None:
            return ReposResults.NotSelected
        return progress