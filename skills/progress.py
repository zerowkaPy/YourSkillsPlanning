from typing import Annotated

from fastapi import Depends, Path, Query, Header
from fastapi import HTTPException
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import Skill, Progress, User
from db.connect import get_db
from route.routers import user_router
from middlwares.auth import get_user_id


@user_router.get("/progress/")
async def global_progress(
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):
    if user_id == "bot":
        subq = select(User.user_id).where(User.telegram_id == telegram_id).scalar_subquery()
        stmt = select(Progress, Skill.name).join(Skill, Progress.skill_id == Skill.id
                                             ).where(Progress.user_id == subq)
    else:
        stmt = select(Progress, Skill.name).join(Skill, Progress.skill_id == Skill.id
                                             ).where(Progress.user_id == user_id)
    res = await session.execute(stmt)
    response = []
    for progress, skill_name in res.all():
        response.append(
            {   
                "name":skill_name,
                "created_at":progress.created_at,
                "total_time":progress.total_time
                }
        )
    return response

@user_router.patch("/progress/{skill_name}")
async def edit_progress(
    session:Annotated[AsyncSession, Depends(get_db)],
    user_id:Annotated[int|str, Depends(get_user_id)],
    skill_name:Annotated[str, Path(max_length=35)],
    telegram_id:Annotated[int|None, Header()] = None,
    reduce:Annotated[bool, Query()] = False,
    add:Annotated[bool, Query()] = False
    ):

    if reduce == add:
        raise HTTPException(status_code=400,
                            detail="You must set exactly one of 'reduce' or 'add' to True")
    
    if user_id == "bot":
        get_user = select(User.user_id).where(User.telegram_id == telegram_id).scalar_subquery()
        subq = select(Skill.id).where(
        and_(Skill.name == skill_name),
            Skill.user_id == get_user).scalar_subquery()
    else:
        subq = select(Skill.id).where(
            and_(Skill.name == skill_name),
                Skill.user_id == user_id).scalar_subquery()
    stmt = update(Progress).where(Progress.skill_id == subq)
    if reduce:
        stmt = stmt.values(total_time=Progress.total_time - 1)
    elif add:
        stmt = stmt.values(total_time= Progress.total_time + 1)
    
    await session.execute(stmt)
    await session.commit()
    return "edited"


