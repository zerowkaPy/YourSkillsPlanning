from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from jose import jwt, JWTError
from fastapi.responses import JSONResponse

from src.enums.auth_enum import AuthType
from src.config import settings
from src.repos.users_repo import UserRepo
from src.db.connect import SessionLocal


SECRET_KEY = settings.jwt_secret_key
MY_API_KEY = settings.my_api_key
ALGORITHM = "HS256"

PUBLIC_PATHS = {
    "/login/",
    "/register/",
    "/login/bot/confirm",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/favicon.ico"
}

class AuthBotMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        token = request.cookies.get("access_token_cookie")
        x_api_key = request.headers.get("x-api-key")
        if x_api_key and x_api_key != MY_API_KEY:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid API key"}
                )
        elif x_api_key:
            request.state.user_id = "bot"
            return await call_next(request)

        if not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "No token"}
            )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user_id = int(payload["sub"])
        except JWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )
        return await call_next(request)
    

async def auth_middleware(request: Request, call_next):
    async with SessionLocal() as session:
        request.state.db = session
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)
    
        x_api_key = request.headers.get("x-api-key")
        if x_api_key == MY_API_KEY:
            telegram_id = request.headers.get("telegram_id")
            if telegram_id is None:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "You must add telegram-id to headers."})
                
            
            result = await UserRepo.resolve_user_id(session=session, telegram_id=int(telegram_id))
            if result is None:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "A user with given telegram-id was not found."})
            request.state.auth_type = AuthType.Bot
            request.state.user_id = result
            return await call_next(request)
        
        elif x_api_key and x_api_key != MY_API_KEY:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid API key."}
            )
        
        token = request.cookies.get("access_token_cookie")
        if token is None:
            return JSONResponse(
                status_code=401,
                content={"detail": "No token."})
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.auth_type = AuthType.User
            request.state.user_id = int(payload["sub"])

        except JWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token."}
            )
        return await call_next(request)
 

