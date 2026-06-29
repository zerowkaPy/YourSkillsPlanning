from typing import Annotated, Any

from fastapi import Depends, Path, Query
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.tools.user_dependency import get_current_user
from src.tools.db_dependency import get_session
from src.services import progress_service


progress_router = APIRouter()

@progress_router.get("/progress/")
async def global_progress(
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[dict[str, Any], Depends(get_current_user)]):
    
    return await progress_service.global_progress(session, user)
    
@progress_router.patch("/progress/{skill_id}")
async def edit_progress(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[dict[str, Any], Depends(get_current_user)],
    skill_id: Annotated[int, Path()],
    reduce: Annotated[bool, Query()] = False,
    add: Annotated[bool, Query()] = False):

    return await progress_service.edit_progress(session, user, skill_id, reduce, add)

