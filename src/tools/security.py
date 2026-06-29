from sqlalchemy import select
from authx import AuthX, AuthXConfig
from passlib.context import CryptContext

from src.db.tables.user import UserOrm
from src.db.connect import  SessionLocal
from src.config import settings


JWT_SECRET_KEY = settings.jwt_secret_key

config = AuthXConfig()
config.JWT_SECRET_KEY = JWT_SECRET_KEY
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_COOKIE_NAME = "access_token_cookie"

security = AuthX(config=config)

@security.set_subject_getter
async def get_user_from_uid(uid: str, **kwargs):
    async with SessionLocal() as session:
        result = await session.execute(
            select(UserOrm.user_id).where(UserOrm.user_id == int(uid))
        )
        return result.scalar_one_or_none()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
