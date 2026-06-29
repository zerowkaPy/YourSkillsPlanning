from sqlalchemy import delete, or_, ScalarSelect
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.db.tables.relation import RelationOrm


class RelationsRepo:

    @classmethod
    async def create_relation(cls, *, parent_id:int, child_id:int, session:AsyncSession, user_id:int|None):
        stmt = insert(RelationOrm).values(
            parent_skill_id=parent_id,
            child_skill_id=child_id,
            user_id=user_id
            ).on_conflict_do_nothing()
        await session.execute(stmt)
        await session.commit()


    @classmethod
    async def delete_skill(cls, *, session: AsyncSession, skill_id: int):
        try:
            stmt = delete(RelationOrm).where(
                        or_(
                            RelationOrm.child_skill_id == skill_id,
                            RelationOrm.parent_skill_id == skill_id)
                            )
            await session.execute(stmt)
            await session.commit()
            return True
        except SQLAlchemyError:
            await session.rollback()
            return False