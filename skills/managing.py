from typing import Annotated

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy import Result, select, insert, delete, update
from sqlalchemy.orm import sessionmaker, Session

from db.tables import Skill
from db.sync_engine import engine
from models.skill import SkillModel

skill_router = APIRouter()

SessionLocal = sessionmaker(engine)

async def get_db():
    with SessionLocal() as session:
        yield session

@skill_router.get("/skills/")
async def get_all(session:Annotated[Session, Depends(get_db)]):
    stmt = select(Skill)
    result:Result[tuple[Skill]] = session.execute(stmt)
    response = []
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

@skill_router.post("/skills/")
async def create_skill(skill:SkillModel, session:Annotated[Session, Depends(get_db)]):
    stmt = insert(Skill).values(
        name=skill.name,
        desc=skill.desc,
        weight=skill.weight)
    
    session.execute(stmt)
    session.commit()
    return "skill added"


@skill_router.patch("/skills/{skill_name}")
async def edit_skill(
    session:Annotated[Session, Depends(get_db)],
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
    
    session.execute(stmt)
    session.commit()
    return "edited"


@skill_router.delete("/skills/{skill_name}")
async def delete_skill(skill_name:str, session:Annotated[Session, Depends(get_db)]):
    stmt = delete(Skill).where(Skill.name == skill_name)
    session.execute(stmt)
    session.commit()
    return "deleted"