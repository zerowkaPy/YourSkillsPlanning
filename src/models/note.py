from pydantic import BaseModel, ConfigDict
from datetime import datetime

from src.models.skill import SkillRelationship

class NoteBase(BaseModel):
    id: int
    skill_id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NoteResponse(NoteBase):
    skill: SkillRelationship
