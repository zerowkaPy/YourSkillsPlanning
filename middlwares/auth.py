from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from jose import jwt, JWTError

from envs import JWT_SECRET_KEY

SECRET_KEY = JWT_SECRET_KEY
ALGORITHM = "HS256"

PUBLIC_PATHS = {
    "/login/",
    "/register/",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/favicon.ico"
}

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        token = request.cookies.get("access_token_cookie")

        if not token:
            raise HTTPException(status_code=401, detail="No token")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user_id = int(payload["sub"])

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)