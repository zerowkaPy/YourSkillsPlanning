from typing import Annotated, Any

from fastapi import Depends, Path, status
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.skill import SkillBase
from src.tools.user_dependency import get_current_user
from src.tools.db_dependency import get_session
from src.services import skills_service


skill_router = APIRouter()

@skill_router.get("/skills/")
async def get_all_skills(
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[dict[str, Any], Depends(get_current_user)]):
    
    return await skills_service.get_all_skills(session, user)

    
@skill_router.post("/skills/", status_code=status.HTTP_201_CREATED)
async def create_skill(
        skill: SkillBase,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[dict[str, Any], Depends(get_current_user)]):
    
    return await skills_service.create_skill(skill, session, user)
   

@skill_router.patch("/skills/{skill_id}")
async def edit_skill(
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[dict[str, Any], Depends(get_current_user)],
        skill_id: Annotated[int, Path()],
        skill: SkillBase,):

    return await skills_service.edit_skill(session, user, skill_id, skill)
    


@skill_router.delete("/skills/{skill_id}")
async def delete_skill(
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[dict[str, Any], Depends(get_current_user)],
        skill_id: int):
    
    return await skills_service.delete_skill(session, user, skill_id)


    