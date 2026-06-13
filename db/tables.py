from sqlalchemy import VARCHAR, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from zoneinfo import ZoneInfo

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    user_id:Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(50), unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    password_hash: Mapped[str] = mapped_column(VARCHAR(255))


class Skill(Base):
    __tablename__ = "skills"
    __table_args__ = (
        UniqueConstraint("user_id", "name"),
    )
    id:Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    name:Mapped[str] = mapped_column(VARCHAR(35))
    desc:Mapped[str] = mapped_column(VARCHAR(200))
    weight:Mapped[int]

    def __repr__(self):
        return f"Skill(id={self.id}, name={self.name}, desc={self.desc}, weight={self.weight})"

class Relation(Base):
    __tablename__ = "relations"
    __table_args__ = (
    UniqueConstraint(
        "user_id",
        "parent_skill_id",
        "child_skill_id"
        ),
    )
    user_id:Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    parent_skill_id:Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True)
    child_skill_id:Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True)


class Progress(Base):
    __tablename__ = "progress"
    user_id:Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        primary_key=True)
    skill_id:Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True)
    created_at:Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Europe/Kyiv")))
    total_time:Mapped[int] = mapped_column(Integer(), default=0)

    def __repr__(self):
        return f"Progress(skill_id={self.skill_id}, created_at={self.created_at}, total_time={self.total_time})"
