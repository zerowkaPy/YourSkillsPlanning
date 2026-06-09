import logging
import sys
from typing import Annotated

from fastapi import Body, FastAPI
from sqlalchemy import text
from sqladmin import Admin, ModelView

import envs
from db.sync_engine import engine
from db.tables import Base, Skill
from models.skill import SkillModel

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

app = FastAPI()
admin = Admin(app, engine)


class SkillsAdmin(ModelView, model=Skill):
    name = "Skill"
    name_plural = "Skills"
    icon = "fa-solid fa-chart-bar"
    column_list = [Skill.name, Skill.desc, Skill.weight]

admin.add_view(SkillsAdmin)

Base.metadata.create_all(engine)

@app.get("/planning/skills/{id}")
async def get_skill(id:int):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM user_skills WHERE id = :id"), {"id":id})
    row = result.fetchone()
    if not row:
        return {}
    
    data = {
        "name":row.name,
        "time_slot":row.time_slot,
    }

    if row.target:
        data.update(target=row.target)
    return data


@app.get("/planning/skills")
async def skills():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROm user_skills"))

    skills = {"skills":[]}


    for row in result:  
        skills["skills"].append(
            {
                "name":row.name,
                "time_slot":row.time_slot,
                "target":row.target
            }
        )
    return skills


@app.post("/planning/new-skills")
async def new_skill(skill: Annotated[SkillModel, Body(embed=True)]):
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO user_skills (name, time_slot, target) " \
        "VALUES(:name, :time_slot, :target)"), 
            {"name":skill.name, "time_slot":skill.time_slot, "target":skill.target})
