from typing import Annotated, Any

from fastapi import Depends, Path, Header
from sqlalchemy.ext.asyncio import AsyncSession

from db.connect import get_db
from models.skill import SkillModel
from middlwares.auth import get_user_id

from repos.skills_repo import SkillRepo, SkillRepoBot
from repos.progress_repo import ProgressRepo
from repos.relations_repo import RelationsRepo
from constants import BOT_ID


async def get_all_skills(
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None,
        only_names:bool = False) -> list[dict[str, Any]]:
    
    response = []
    if user_id == BOT_ID:
        result = await SkillRepoBot.get_all_skills(session=session, telegram_id=telegram_id)
    else:
        result = await SkillRepo.get_all_skills(session=session, user_id=user_id)

    if only_names:
        for skill in result:
            response.append({"name":skill.name})
    else:
        for skill in result:
            response.append(
                {
                "name":skill.name,
                "desc":skill.desc,
                "weight":skill.weight
                }
            )
    return response


async def create_skill(
        skill:SkillModel,
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):
    
    if user_id == BOT_ID:
        skill_id = await SkillRepoBot.create_skill(session=session, skill=skill, telegram_id=telegram_id,)
    else:
        skill_id = await SkillRepo.create_skill(session=session, skill=skill, user_id=user_id)
    await ProgressRepo.create_skill(session=session, user_id=user_id, skill_id=skill_id)
    return "Skill created"


async def edit_skill(
    session:Annotated[AsyncSession, Depends(get_db)],
    skill_name:Annotated[str, Path(max_length=35)],
    skill:SkillModel,
    user_id:Annotated[int|str, Depends(get_user_id)],
    telegram_id:Annotated[int|None, Header()] = None):

    values = skill.model_dump(exclude_none=True)

    if user_id == BOT_ID:
        return await SkillRepoBot.edit_skill(session=session, skill_name=skill_name, telegram_id=telegram_id, values=values)
    
    await SkillRepo.edit_skill(session=session, skill_name=skill_name, user_id=user_id, values=values)
    return "Skill edited"
        

async def delete_skill(
        session:Annotated[AsyncSession, Depends(get_db)],
        skill_name:str,
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):
    
    if user_id == BOT_ID:
        skill_id = SkillRepoBot.get_skill_id_by_name(skill_name=skill_name, telegram_id=telegram_id)
    else:
        skill_id = SkillRepo.get_skill_id_by_name(skill_name=skill_name, user_id=user_id) # type: ignore
    
    await ProgressRepo.delete_skill(session=session, skill_id=skill_id)
    await RelationsRepo.delete_skill(session=session, skill_id=skill_id)
    await SkillRepo.delete_skill(session=session, skill_id=skill_id)
    return "Skill deleted"
