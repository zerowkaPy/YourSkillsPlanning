from datetime import datetime

from sqlalchemy import ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.orm_base import Base
from src.db.tables.skill import SkillOrm


class ProgressOrm(Base):
    __tablename__ = "progress"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        primary_key=True)
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    total_time: Mapped[int] = mapped_column(Integer(), default=0)
    skill: Mapped["SkillOrm"] = relationship(lazy="selectin")

    def __repr__(self):
        return f"Progress(skill_id={self.skill_id}, created_at={self.created_at}, total_time={self.total_time})"
    