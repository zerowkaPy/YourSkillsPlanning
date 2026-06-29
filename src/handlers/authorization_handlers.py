from typing import Annotated
import secrets
from zoneinfo import ZoneInfo
from datetime import datetime

from fastapi import Depends, HTTPException, Response, Request, Header, Path, APIRouter
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.credent import CredentModel, LoginData, LinkData
from src.db.tables.user import UserOrm
from src.db.tables.tglink import TGLinkOrm
from src.tools.db_dependency import get_session
from src.config import settings
from src.tools.security import security, config, pwd_context


MY_API_KEY = settings.my_api_key

auth_router = APIRouter()

@auth_router.post("/register/")
async def sign_up(
    credent: CredentModel,
    session: Annotated[AsyncSession, Depends(get_session)]):

    query = select(UserOrm).where(UserOrm.email == credent.email)
    result = await session.execute(query)
    user = result.one_or_none()

    if user is None:
        hashed_pwd = pwd_context.hash(credent.password)
        stmt = insert(UserOrm).values(
            username=credent.username,
            email=credent.email,
            password_hash=hashed_pwd)
        await session.execute(stmt)
        await session.commit()
    else:
        raise HTTPException(status_code=409, detail="User with this email already exists")
    

@auth_router.post("/login/")
async def login(
        userdata: LoginData,
        session: Annotated[AsyncSession, Depends(get_session)],
        response: Response):
    
    query = select(UserOrm).where(UserOrm.email == userdata.email)
    result = await session.execute(query)
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


@auth_router.post("/login/bot/")
async def login_bot(
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request):

    token = secrets.token_urlsafe(16)
    stmt = insert(TGLinkOrm).values(
        user_id=request.state.user_id,
        token=token
    )
    await session.execute(stmt)
    await session.commit()
    return token


@auth_router.post("/login/bot/confirm")
async def confirm_link(
    session: Annotated[AsyncSession, Depends(get_session)],
    data: LinkData,
    x_api_key: Annotated[str|None, Header()] = None
    ):

    if x_api_key != MY_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    current_time = datetime.now(ZoneInfo("UTC"))
    select_stmt = select(TGLinkOrm).where(TGLinkOrm.token == data.token, TGLinkOrm.expires_at > current_time)
    result = await session.execute(select_stmt)
    link = result.scalar_one_or_none()
    if link is None:
        raise HTTPException(status_code=401, detail="Link does not exist or link is expired")
    elif link.used:
        raise HTTPException(status_code=401, detail="Link already used")
    update_link = update(TGLinkOrm).where(TGLinkOrm.token == data.token).values(used=True)
    update_user = update(UserOrm).where(UserOrm.user_id == link.user_id).values(telegram_id=data.telegram_id)
    await session.execute(update_link)
    await session.execute(update_user)
    await session.commit()
    return "Confirmed"


@auth_router.post("/login/bot/check{telegram_user_id}")
async def check_tg_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    telegram_user_id: Annotated[int, Path()],
    x_api_key: Annotated[str|None, Header()] = None
    ):

    if x_api_key != MY_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    stmt = select(UserOrm.telegram_id).where(UserOrm.telegram_id == telegram_user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        return False
    return True

@auth_router.delete("/login/bot/{telegram_user_id}")
async def delete_user(
        session: Annotated[AsyncSession, Depends(get_session)],
        telegram_user_id: Annotated[int, Path()],
        x_api_key: Annotated[str|None, Header()] = None
):
    if x_api_key != MY_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    del_stmt = update(UserOrm).where(UserOrm.telegram_id == telegram_user_id).values(telegram_id=None)
    await session.execute(del_stmt)
    await session.commit()

@auth_router.get("/login/bot/all")
async def all_users(
        session: Annotated[AsyncSession, Depends(get_session)],
        x_api_key: Annotated[str|None, Header()] = None
):
    if x_api_key != MY_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    select_stmt = select(UserOrm.telegram_id)
    result = await session.execute(select_stmt)
    rows = result.scalars()
    return [id for id in rows]