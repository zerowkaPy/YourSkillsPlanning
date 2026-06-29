from fastapi import FastAPI

def setup_middlewares(app: FastAPI):
    from src.middlwares.auth import auth_middleware

    app.middleware("http")(auth_middleware)