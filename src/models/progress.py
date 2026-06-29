from pydantic import BaseModel, ConfigDict
from datetime import datetime

from src.models.skill import SkillRelationship


class ProgressResponse(BaseModel):
    created_at: datetime
    total_time: int
    skill: SkillRelationship

    model_config = ConfigDict(from_attributes=True)