from typing import Annotated

from fastapi import Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from authx import AuthX, AuthXConfig, RequestToken
from passlib.context import CryptContext

from route.routers import user_router
from models.credent import CredentModel, LoginData
from db.tables import User, Skill
from db.connect import get_db, SessionLocal
from envs import JWT_SECRET_KEY

config = AuthXConfig()
config.JWT_SECRET_KEY = JWT_SECRET_KEY
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_COOKIE_NAME = "access_token_cookie"

security = AuthX(config=config)

@security.set_subject_getter
async def get_user_from_uid(uid: str, **kwargs):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User.user_id).where(User.user_id == int(uid))
        )
        return result.scalar_one_or_none()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


@user_router.post("/register/")
async def sign_up(credent:CredentModel, session:Annotated[AsyncSession, Depends(get_db)]):
    select_stmt = select(User).where(User.email == credent.email)
    result = await session.execute(select_stmt)
    user = result.one_or_none()
    if user is None:
        hashed_pwd = pwd_context.hash(credent.password)

        insert_stmt = insert(User).values(
            username=credent.username,
            email=credent.email,
            password_hash=hashed_pwd)
        await session.execute(insert_stmt)
        await session.commit()
    else:
        raise HTTPException(status_code=409, detail="User with this email already exists")


@user_router.post("/login/")
async def login(userdata:LoginData, session:Annotated[AsyncSession, Depends(get_db)], response:Response):
    select_stmt = select(User).where(User.email == userdata.email)
    result = await session.execute(select_stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect email")
    else:
        if pwd_context.verify(userdata.password, user.password_hash):
            token = security.create_access_token(uid=str(user.user_id))
            response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
            return {"access_token" : token}
        else:
            raise HTTPException(status_code=401, detail="Incorrect password")


@user_router.get("/private/")
async def private(
    session:Annotated[AsyncSession, Depends(get_db)],
    subject: str | None = Depends(security.get_current_subject)
    ):
    
    if subject is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated. Token is missing or invalid"
        )

    stmt = select(Skill).where(Skill.user_id == subject)
    result = await session.execute(stmt)
    rows = result.scalars()
    response = []
    for skill in rows:
        response.append({
            "name":skill.name,
            "desc":skill.desc,
            "weight":skill.weight
        })

    return response