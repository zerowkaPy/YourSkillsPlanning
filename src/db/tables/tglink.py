from sqlalchemy import VARCHAR, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from src.db.orm_base import Base


class TGLinkOrm(Base):
    __tablename__ = "tg_links"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    token: Mapped[str] = mapped_column(VARCHAR(128))
    expires_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now()) + INTERVAL '10 minutes'"))
    used: Mapped[bool] = mapped_column(default=False)