from typing import Annotated
from pydantic import BaseModel,Field

class SkillModel(BaseModel):
    name:Annotated[str, Field(max_length=35)]
    desc:Annotated[str, Field(max_length=200)]
    weight:Annotated[int, Field(ge=0, le=5)]

