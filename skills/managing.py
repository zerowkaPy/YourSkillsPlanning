from typing import Annotated

from fastapi import Depends, Path, Header
from sqlalchemy import Result, select, delete, update, or_, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import Skill, Progress, Relation, User
from db.connect import get_db, SessionLocal
from models.skill import SkillModel
from route.routers import user_router
from skills.relations import build_relations
from middlwares.auth import get_user_id

@user_router.get("/skills/")
async def get_all(
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None,
        only_names:bool = False) -> list[dict[str, str|int] | str]:
    if user_id == "bot":
        subq = select(User.user_id).where(User.telegram_id == telegram_id).scalar_subquery()
        stmt = select(Skill).where(Skill.user_id == subq)
    else:
        stmt = select(Skill).where(Skill.user_id == user_id)
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
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):
    
    if user_id == "bot":
        get_user = select(User.user_id).where(User.telegram_id == telegram_id)
        user = await session.execute(get_user)
        user_id = user.scalar_one()
    skill_stmt = insert(Skill).values(
        user_id=user_id,
        name=skill.name,
        desc=skill.desc,
        weight=skill.weight).returning(Skill.id)
    
    result = await session.execute(skill_stmt)
    await session.commit()

    skill_id = result.scalar_one()
    progress_stmt = insert(Progress).values(
        user_id=user_id,
        skill_id=skill_id
        )
    await session.execute(progress_stmt)
    await session.commit()
    return "skill added"


@user_router.patch("/skills/{skill_name}")
async def edit_skill(
    session:Annotated[AsyncSession, Depends(get_db)],
    skill_name:Annotated[str, Path(max_length=35)],
    skill:SkillModel,
    user_id:Annotated[int|str, Depends(get_user_id)],
    telegram_id:Annotated[int|None, Header()] = None):

    values = {}
    if skill.name is not None:
        values.update(name = skill.name)
    if skill.desc is not None:
        values.update(desc = skill.desc)
    if skill.weight is not None:
        values.update(weight = skill.weight)

    if user_id == "bot":
        subq = select(User.user_id).where(User.telegram_id == telegram_id).scalar_subquery()
        stmt = update(Skill).where(
        and_(Skill.name == skill_name),
            Skill.user_id == subq).values(**values)
    else:
        stmt = update(Skill).where(
            and_(Skill.name == skill_name),
                Skill.user_id == user_id).values(**values)
    await session.execute(stmt)
    await session.commit()
    return "skill edited"


@user_router.delete("/skills/{skill_name}")
async def delete_skill(
        skill_name:str,
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int|str, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):
    
    if user_id == "bot":
        subq = select(Skill.id).where(
            and_(Skill.name == skill_name,
                User.telegram_id == telegram_id)).scalar_subquery()
    else:
        subq = select(Skill.id).where(
                                and_(Skill.name == skill_name),
                                    Skill.user_id == user_id).scalar_subquery()
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

    stmt = delete(Skill).where(
        and_(Skill.name == skill_name),
            Skill.id == subq)
    await session.execute(stmt)
    await session.commit()
    return "deleted"


@user_router.get("/skills/graph")
async def get_graph(
        session:Annotated[AsyncSession, Depends(get_db)],
        user_id:Annotated[int, Depends(get_user_id)],
        telegram_id:Annotated[int|None, Header()] = None):
    
    if user_id == "bot":
        get_user = select(User.user_id).where(User.telegram_id == telegram_id)
        res = await session.execute(get_user)
        user_id_from_tg = res.scalar_one()
        stmt = select(Skill).where(Skill.user_id == user_id_from_tg)
    else:
        stmt = select(Skill).where(Skill.user_id == user_id)
    result:Result[tuple[Skill]] = await session.execute(stmt)
    skills = []
    skills_id = {}
    for row in result:
        skill = row[0]
        skills.append(skill.name)
        skills_id[skill.name] = skill.id

    if user_id == "bot":
        await insert_relations(session, skills, skills_id, user_id_from_tg)
    else:
        await insert_relations(session, skills, skills_id, user_id)

    ParentSkill = aliased(Skill)
    ChildSkill = aliased(Skill)

    if user_id == "bot":
        select_stmt = (
            select(
                Relation,
                ParentSkill.name.label("parent_name"),
                ChildSkill.name.label("child_name"),
            )
            .join(ParentSkill, Relation.parent_skill_id == ParentSkill.id)
            .join(ChildSkill, Relation.child_skill_id == ChildSkill.id)
        ).where(Relation.user_id == user_id_from_tg)
    else:
        select_stmt = (
            select(
                Relation,
                ParentSkill.name.label("parent_name"),
                ChildSkill.name.label("child_name"),
            )
            .join(ParentSkill, Relation.parent_skill_id == ParentSkill.id)
            .join(ChildSkill, Relation.child_skill_id == ChildSkill.id)
        ).where(Relation.user_id == user_id)

    result1 = await session.execute(select_stmt)
    response = []
    for row in result1:
        print(row)
        response.append({
            "parent": row.parent_name,
            "child": row.child_name,
        })
    return response


async def insert_relations(
        session:AsyncSession,
        skills:list[str],
        skills_id:dict[str, int],
        user_id:int):
    
    relations = await build_relations(skills)
    edges = relations["edges"]
    stmt_insert = insert(Relation)
    for edge in edges:
        parent = edge["parent"]
        child = edge["child"]
        parent_id = skills_id[parent]
        child_id = skills_id[child]
        stmt = stmt_insert.values(
            parent_skill_id=parent_id,
            child_skill_id=child_id,
            user_id=user_id
            ).on_conflict_do_nothing()
        await session.execute(stmt)
    await session.commit()
    