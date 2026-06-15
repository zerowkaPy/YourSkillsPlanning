from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from jose import jwt, JWTError
from fastapi.responses import JSONResponse


from envs import JWT_SECRET_KEY, MY_API_KEY
assert JWT_SECRET_KEY is not None
assert MY_API_KEY is not None

SECRET_KEY = JWT_SECRET_KEY
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

class AuthMiddleware(BaseHTTPMiddleware):
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
    
def get_user_id(request:Request):
    user_id = request.state.user_id
    if user_id == "bot":
        return "bot"
    else:
        return user_id
