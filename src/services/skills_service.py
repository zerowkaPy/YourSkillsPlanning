from typing import Annotated, Any

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.skill import SkillBase, SkillResponse
from src.tools.user_dependency import get_current_user
from src.tools.db_dependency import get_session

from src.repos.skills_repo import SkillRepo
from src.repos.progress_repo import ProgressRepo
from src.repos.relations_repo import RelationsRepo
from src.repos.notes_repo import NotesRepo
from src.errors_handling.funcs import throw_409, throw_500, throw_404
from src.enums.alchemy_exceptions import AlchemyExcs
from src.enums.repos_exceptions import ReposResults


FAIL_EXCEPTIONS = {
    AlchemyExcs.IntegrityErr : "Skill with this name already exist",
    AlchemyExcs.DataErr : "Given data is not correct"}

async def get_all_skills(
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[dict[str, Any], Depends(get_current_user)]
        ) -> dict[str, list[SkillResponse]] | Exception:
    
    user_id = user["user_id"]
    
    result = await SkillRepo.get_all_skills(session=session, user_id=user_id)

    if not result:
        return {"skills" : []}

    skills = []
    for skill in result:
        skills.append(SkillResponse.model_validate(skill))
    return {"skills" : skills}


async def create_skill(
        skill: SkillBase,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[dict[str, Any], Depends(get_current_user)]):

    user_id = user["user_id"]
    
    skill_returned = await SkillRepo.create_skill(session=session, skill=skill, user_id=user_id)
    if skill_returned is AlchemyExcs.IntegrityErr:
        raise throw_409(FAIL_EXCEPTIONS[AlchemyExcs.IntegrityErr])
    elif skill_returned is AlchemyExcs.DataErr:
        raise throw_409(FAIL_EXCEPTIONS[AlchemyExcs.DataErr])
    elif skill_returned is AlchemyExcs.GlobalErr:
        raise throw_500()
    
    skill_id = skill_returned.id
    await ProgressRepo.create_progress(session=session, user_id=user_id, skill_id=skill_id)
    return SkillResponse.model_validate(skill_returned)


async def edit_skill(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[dict[str, Any], Depends(get_current_user)],
    skill_id: Annotated[int, Path()],
    skill: SkillBase):

    user_id = user["user_id"]
    values = skill.model_dump(exclude_none=True)

    result = await SkillRepo.edit_skill(session=session, skill_id=skill_id, user_id=user_id, values=values)
    if result is ReposResults.NotUpdated:
        raise throw_409("Skill was not updated")
    if not result:
        raise throw_500()
    return SkillResponse.model_validate(result)
        

async def delete_skill(
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[dict[str, Any], Depends(get_current_user)],
        skill_id: Annotated[int, Path()]):
    
    user_id = user["user_id"]

    fetched_skill = await SkillRepo.get_skill_by_id(session=session, user_id=user_id, skill_id=skill_id)
    if fetched_skill is None:
        raise throw_404(f"Skill was not found with given id: {skill_id}")
    
    results = (
    await ProgressRepo.delete_progress(session=session, skill_id=skill_id),
    await RelationsRepo.delete_skill(session=session, skill_id=skill_id),
    await NotesRepo.delete_all_notes(session=session, skill_id=skill_id)
    )

    skill = await SkillRepo.delete_skill(session=session, skill_id=skill_id)
    if not all(results) or not skill:
        raise throw_500()
    return SkillResponse.model_validate(skill)
