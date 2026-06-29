from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import  Mapped, mapped_column

from src.db.orm_base import Base


class RelationOrm(Base):
    __tablename__ = "relations"
    __table_args__ = (
    UniqueConstraint(
        "user_id",
        "parent_skill_id",
        "child_skill_id"
        ),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    parent_skill_id:Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True)
    child_skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True)