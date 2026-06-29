from sqlalchemy import VARCHAR
from sqlalchemy.orm import  Mapped, mapped_column

from src.db.orm_base import Base


class UserOrm(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(50), unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    password_hash: Mapped[str] = mapped_column(VARCHAR(255))
    telegram_id: Mapped[int] = mapped_column(nullable=True)