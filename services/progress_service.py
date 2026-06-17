from typing import Annotated

from fastapi import Depends, Path, Query, Header
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.connect import get_db
from middlwares.auth import get_user_id
from constants import BOT_ID
from repos.progress_repo import ProgressRepo, ProgressRepoBot


async def global_progress(
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):

    response = []

    if user_id == BOT_ID:
        progress_list = await ProgressRepoBot.all_skills(session=session, telegram_id=telegram_id)
    else:
        progress_list = await ProgressRepo.all_skills(session=session, user_id=user_id)
        
    response = []
    for progress, skill_name in progress_list.all():
        response.append(
            {   
                "name":skill_name,
                "created_at":progress.created_at,
                "total_time":progress.total_time
                }
        )
    return response


async def edit_progress(
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int|str, Depends(get_user_id)],
        skill_name:Annotated[str, Path(max_length=35)],
        telegram_id:Annotated[int|None, Header()] = None,
        reduce:Annotated[bool, Query()] = False,
        add:Annotated[bool, Query()] = False):

    if reduce == add:
        raise HTTPException(status_code=400,
                            detail="You must set exactly one of 'reduce' or 'add' to True")
    if add:
        if user_id == BOT_ID:
            await ProgressRepoBot.add_to_progress(session=session, skill_name=skill_name, telegram_id=telegram_id)
        else:
            await ProgressRepoBot.reduce_progress(session=session, skill_name=skill_name, telegram_id=telegram_id)
    else:
        if user_id == BOT_ID:
            await ProgressRepo.add_to_progress(session=session, skill_name=skill_name, user_id=user_id) # type: ignore
        else:
            await ProgressRepo.reduce_progress(session=session, skill_name=skill_name, user_id=user_id) # type: ignore
    return "Progress edited"