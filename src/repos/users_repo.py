from sqlalchemy import select, ScalarSelect
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.tables.user import UserOrm



class UserRepo:

    @classmethod
    def resolve_user_id_subq(cls, *, telegram_id:int|None) -> ScalarSelect[int]:
        return select(UserOrm.user_id).where(UserOrm.telegram_id == telegram_id).scalar_subquery()
    

    @classmethod
    async def resolve_user_id(cls, *, session:AsyncSession, telegram_id:int|None) -> int|None: 
        query = select(UserOrm.user_id).where(UserOrm.telegram_id == telegram_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()