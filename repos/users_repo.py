from sqlalchemy import select, ScalarSelect
from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import User



class UsersRepoBot:

    @classmethod
    def user_id_subq(cls, *, telegram_id:int|None) -> ScalarSelect[int]:
        return select(User.user_id).where(User.telegram_id == telegram_id).scalar_subquery()
    

    @classmethod
    async def fetch_user_id(cls, *, session:AsyncSession, telegram_id:int|None) -> int|None: 
        stmt = select(User.user_id).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()