from typing import Annotated

from fastapi import Depends, Path, Header
from sqlalchemy.ext.asyncio import AsyncSession

from db.connect import get_db
from models.skill import SkillModel
from route.routers import user_router
from middlwares.auth import get_user_id

from services import skills_service

@user_router.get("/skills/")
async def get_all_skills(
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None,
        only_names:bool = False):
    
    return await skills_service.get_all_skills(session, user_id, telegram_id, only_names)

    

@user_router.post("/skills/")
async def create_skill(
        skill:SkillModel,
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):
    
    return await skills_service.create_skill(skill, session, user_id, telegram_id)
   

@user_router.patch("/skills/{skill_name}")
async def edit_skill(
        session:Annotated[AsyncSession, Depends(get_db)],
        skill_name:Annotated[str, Path(max_length=35)],
        skill:SkillModel,
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):

    return await skills_service.edit_skill(session, skill_name, skill, user_id, telegram_id)
    


@user_router.delete("/skills/{skill_name}")
async def delete_skill(
        session:Annotated[AsyncSession, Depends(get_db)],
        skill_name:str,
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):
    
    return await skills_service.delete_skill(session, skill_name, user_id, telegram_id)


    