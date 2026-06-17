from typing import Annotated
from pydantic import BaseModel, Field

class SkillModel(BaseModel):
    name:Annotated[str|None, Field(max_length=35)] = None
    desc:Annotated[str|None, Field(max_length=200)] = None
    weight:Annotated[int|None, Field(ge=0, le=5)] = None
