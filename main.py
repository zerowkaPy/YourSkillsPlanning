from typing import Annotated

from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class Skill(BaseModel):
    name:str
    time_slot:int       #days number
    target:str|None = None

@app.post("/planning/new-skills")
async def new_skill(skill:Annotated[Skill, Body(embed=True)]):
    pass