from typing import Annotated, Any

from fastapi import Depends, Path, Query
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.repos.progress_repo import ProgressRepo
from src.errors_handling.funcs import throw_404, throw_409
from src.models.progress import ProgressResponse
from src.enums.repos_exceptions import ReposResults
from src.tools.user_dependency import get_current_user
from src.tools.db_dependency import get_session

async def global_progress(
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[dict[str, Any], Depends(get_current_user)]) -> dict[str, Any]:

    user_id = user["user_id"]
    result = await ProgressRepo.all_progress(session=session, user_id=user_id)
    if not result:
        raise throw_404("No progress found. Maybe no skills have been created yet?")
    
    return {
        "progress" : [ProgressResponse.model_validate(progress) for progress in result]
    }
    

async def edit_progress(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[dict[str, Any], Depends(get_current_user)],
    skill_id: Annotated[int, Path()],
    reduce: Annotated[bool, Query()] = False,
    add: Annotated[bool, Query()] = False):

    if reduce == add:
        raise HTTPException(status_code=400,
                            detail="You must set exactly one of 'reduce' or 'add' to True.")
    
    user_id = user["user_id"]
    if add:
        result = await ProgressRepo.add_to_progress(session=session, skill_id=skill_id, user_id=user_id)
    else:
        result = await ProgressRepo.get_one_progress(session=session, skill_id=skill_id, user_id=user_id)
        if result is ReposResults.NotSelected:
            raise throw_404("No progress found.")
        curent_total_time = result.total_time
        if curent_total_time <= 0:
            raise throw_409("Progress cannot be reduced because it is already 0.")
        result = await ProgressRepo.reduce_progress(session=session, skill_id=skill_id, user_id=user_id)

    if result is ReposResults.NotUpdated:
        raise throw_404("No progress found.")
    return {"progress" : ProgressResponse.model_validate(result)}