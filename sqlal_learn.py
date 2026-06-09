
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

from typing import Optional
DB_URL="postgresql+psycopg://postgres:zerowich@localhost:5000/skills"


engine = create_engine(DB_URL, echo=True, pool_timeout=5)
# metadata_obj = MetaData()

# users = Table(
#     "users",
#     metadata_obj,
#     Column("user_id", Integer, primary_key=True),
#     Column("username", String(20), nullable=False)
# )


# user_skills = Table(

#     "user_skills",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("user_id", ForeignKey("users.user_id"), nullable=False),
#     Column("name", String(50), nullable=False),
#     Column("time_slot", Integer, nullable=False),
#     Column("target", String(250))
# )


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    user_id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(String(20))
    
class User_skills(Base):
    __tablename__ = "user_skills"
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int]
    name:Mapped[str] = mapped_column(String(50))
    time_slot:Mapped[int]
    target:Mapped[Optional[str]] = mapped_column(String(200))

# Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)

# with engine.connect() as conn:
#     conn.execute(text("INSERT INTO users VALUES(:x1, :x2)"), {"x1":444, "x2":"zerow"})
#     conn.commit()

# with engine.connect() as conn:
#     conn.execute(text("""INSERT INTO user_skills
#                       (user_id, name, time_slot, target)
#                         VALUES(:x1, :x2, :x3, :x4)"""), {"x1":444, "x2":"Celery", "x3":2, "x4":"blablabla"})
#     conn.commit()

# with engine.connect() as conn:
#     res1 = conn.execute(text("SELECT * FROM users"))
#     res2 = conn.execute(text("SELECT * FROM user_skills"))

# print(res1.all(), "\n")
# print(res2.all())
    
# metadata_obj.drop_all(engine)