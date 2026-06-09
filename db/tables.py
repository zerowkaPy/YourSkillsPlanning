from sqlalchemy import VARCHAR, Integer, ForeignKey, DATE, Date, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Skill(Base):
    __tablename__ = "skills"
    id:Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True)
    name:Mapped[str] = mapped_column(VARCHAR(35))
    desc:Mapped[str] = mapped_column(VARCHAR(200))
    weight:Mapped[int]


class Relation(Base):
    __tablename__ = "relations"
    parent_skill_id:Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True)
    child_skill_id:Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True)


class Plan(Base):
    __tablename__ = "plan"
    skill_id:Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True)
    created_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    study_date:Mapped[Date] = mapped_column(DATE())
