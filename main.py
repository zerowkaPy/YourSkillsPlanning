import logging
import os
import sys
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Body, FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

load_dotenv(".env")
check_url = DB_URL = os.getenv("DB_URL")
if not check_url:
    logging.error("Environment variable DB_URL wasn't imported")


app = FastAPI()

engine = create_engine(DB_URL, echo=True) # type: ignore

class Skill(BaseModel):
    name: str
    time_slot: int  # days number
    target: str | None = None


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
async def new_skill(skill: Annotated[Skill, Body(embed=True)]):
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO user_skills (name, time_slot, target) " \
        "VALUES(:name, :time_slot, :target)"), 
            {"name":skill.name, "time_slot":skill.time_slot, "target":skill.target})
