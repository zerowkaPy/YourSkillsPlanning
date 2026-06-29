from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from zoneinfo import ZoneInfo

from src.db.orm_base import Base
from src.db.tables import SkillOrm

class NoteOrm(Base):
    __tablename__ = "notes"
    __table_args__ = (
        UniqueConstraint("skill_id", "text"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id"))
    text: Mapped[str] = mapped_column()
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("UTC")))
    skill: Mapped["SkillOrm"] = relationship(lazy="selectin")