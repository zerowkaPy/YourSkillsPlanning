from typing import Annotated

from fastapi import Depends, Path, Query
from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import Skill, Progress
from db.connect import get_db
from route.routers import user_router

@user_router.get("/progress/")
async def global_progress(session:Annotated[AsyncSession, Depends(get_db)]):
    stmt = select(Progress, Skill.name).join(Skill, Progress.skill_id==Skill.id)
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
    skill_name:Annotated[str, Path(max_length=35)],
    reduce:Annotated[bool, Query()] = False,
    add:Annotated[bool, Query()] = False
    ):

    if reduce == add:
        raise HTTPException(status_code=400,
                            detail="You must set exactly one of 'reduce' or 'add' to True")
    subq = select(Skill.id).where(Skill.name == skill_name).scalar_subquery()
    stmt = update(Progress).where(Progress.skill_id == subq)
    if reduce:
        stmt = stmt.values(total_time=Progress.total_time - 1)
    elif add:
        stmt = stmt.values(total_time= Progress.total_time + 1)
    
    await session.execute(stmt)
    await session.commit()
    return "edited"


