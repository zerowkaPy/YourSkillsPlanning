from typing import Annotated
import asyncio

from fastapi import Depends, Query, Path, Request
from sqlalchemy import Result, select, delete, update, or_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import Skill, Progress, Relation
from db.connect import get_db, SessionLocal
from models.skill import SkillModel
from route.routers import user_router
from skills.relations import build_relations
from security import security


@user_router.get("/skills/")
async def get_all(session:Annotated[AsyncSession, Depends(get_db)], only_names:bool = False):
    stmt = select(Skill)
    result:Result[tuple[Skill]] = await session.execute(stmt)
    response = []
    if only_names:
        for row in result:
            skill = row[0]
            response.append(skill.name)
        return response
    
    for row in result:
        skill = row[0]
        response.append(
            {
            "name":skill.name,
            "desc":skill.desc,
            "weight":skill.weight
            }
        )
    return response

@user_router.post("/skills/")
async def create_skill(
    skill:SkillModel,
    session:Annotated[AsyncSession, Depends(get_db)],
    request:Request):
    skill_stmt = insert(Skill).values(
        user_id=request.state.user_id,
        name=skill.name,
        desc=skill.desc,
        weight=skill.weight).returning(Skill.id)
    
    result = await session.execute(skill_stmt)
    await session.commit()

    skill_id = result.scalar_one()
    progress_stmt = insert(Progress).values(
        user_id=request.state.user_id,
        skill_id=skill_id
        )
    await session.execute(progress_stmt)
    await session.commit()

    return "skill added"


@user_router.patch("/skills/{skill_name}")
async def edit_skill(
    session:Annotated[AsyncSession, Depends(get_db)],
    skill_name:Annotated[str, Path(max_length=35)],
    name:Annotated[str|None, Query(max_length=35)] = None,
    desc:Annotated[str|None, Query(max_length=200)] = None,
    weight:Annotated[int|None, Query(ge=0, le=5)] = None):

    values = {}
    if name is not None:
        values.update(name=name)
    if desc is not None:
        values.update(desc=desc)
    if weight is not None:
        values.update(weight=weight)
    stmt = update(Skill).where(Skill.name==skill_name).values(**values)
    
    await session.execute(stmt)
    await session.commit()
    return "edited"


@user_router.delete("/skills/{skill_name}")
async def delete_skill(skill_name:str, session:Annotated[AsyncSession, Depends(get_db)]):
    subq = select(Skill.id).where(Skill.name == skill_name).scalar_subquery()
    progress_stmt = delete(Progress).where(Progress.skill_id == subq)
    await session.execute(progress_stmt)
    await session.commit()

    relat_stmt = delete(Relation).where(
        or_(
            Relation.child_skill_id == subq,
            Relation.parent_skill_id == subq)
    )
    await session.execute(relat_stmt)
    await session.commit()

    stmt = delete(Skill).where(Skill.name == skill_name)
    await session.execute(stmt)
    await session.commit()



@user_router.get("/skills/graph")
async def get_graph(session:Annotated[AsyncSession, Depends(get_db)]):
    stmt = select(Skill)
    result:Result[tuple[Skill]] = await session.execute(stmt)
    skills = []
    skills_id = {}
    for row in result:
        skill = row[0]
        skills.append(skill.name)
        skills_id[skill.name] = skill.id
    await insert_relations(skills, skills_id)

    ParentSkill = aliased(Skill)
    ChildSkill = aliased(Skill)

    stmt = (
        select(
            Relation,
            ParentSkill.name.label("parent_name"),
            ChildSkill.name.label("child_name"),
        )
        .join(ParentSkill, Relation.parent_skill_id == ParentSkill.id)
        .join(ChildSkill, Relation.child_skill_id == ChildSkill.id)
    )

    result1 = await session.execute(stmt)

    response = []
    for row in result1:
        response.append({
            "parent": row.parent_name,
            "child": row.child_name,
        })
    return response


async def insert_relations(skills:list[str], skills_id:dict[str, int]):
    relations = await build_relations(skills)
    edges = relations["edges"]
    stmt_insert = insert(Relation)

    async with SessionLocal() as session:
        for edge in edges:
            parent = edge["parent"]
            child = edge["child"]
            parent_id = skills_id[parent]
            child_id = skills_id[child]
            stmt = stmt_insert.values(
                parent_skill_id=parent_id,
                child_skill_id=child_id
                ).on_conflict_do_nothing()
            await session.execute(stmt)
            await session.commit()
    