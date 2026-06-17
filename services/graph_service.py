from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession


from db.connect import get_db
from AI.graph_building import build_relations
from middlwares.auth import get_user_id


from constants import BOT_ID
from repos.users_repo import UsersRepoBot
from repos.skills_repo import SkillRepo, SkillRepoBot
from repos.relations_repo import RelationsRepo



async def make_graph(
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None) -> list[dict[str, str]]:
    
    skills:dict[str, int] = {}
    if user_id == BOT_ID:
        skills_list = await SkillRepoBot.get_all_skills(session=session, telegram_id=telegram_id)
    else:
        skills_list = await SkillRepo.get_all_skills(session=session, user_id=user_id)

    for skill in skills_list:
        skills.update({skill.name : skill.id})

    if user_id == BOT_ID:
        user_id_from_tg = await UsersRepoBot.fetch_user_id(session=session, telegram_id=telegram_id)
        edges = await insert_relations(session, skills, user_id_from_tg)
    else:
        edges = await insert_relations(session, skills, user_id)
    return edges


async def insert_relations(
        session:AsyncSession,
        skills:dict[str, int],
        user_id:int|None) -> list[dict[str, str]]:
    
    skill_names = list(skills.keys())

    relations = await build_relations(skill_names)
    edges = relations["edges"]
    for edge in edges:
        parent = edge["parent"]
        child = edge["child"]
        parent_id = skills[parent]
        child_id = skills[child]
        await RelationsRepo.create_relation(parent_id=parent_id, child_id=child_id, session=session, user_id=user_id)
    return edges
