from sqlalchemy import VARCHAR, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db.orm_base import Base



class SkillOrm(Base):
    __tablename__ = "skills"
    __table_args__ = (
        UniqueConstraint("user_id", "name"),
    )
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    name: Mapped[str] = mapped_column(VARCHAR(35))
    desc: Mapped[str] = mapped_column(VARCHAR(200))
    weight: Mapped[int]

    def __repr__(self):
        return f"Skill(id={self.id}, name={self.name}, desc={self.desc}, weight={self.weight})"