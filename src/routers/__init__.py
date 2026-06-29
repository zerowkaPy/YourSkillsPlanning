from fastapi import FastAPI

def setup_routers(app: FastAPI):
    from src.handlers.skills_handlers import skill_router
    from src.handlers.progress_handlers import progress_router
    from src.handlers.authorization_handlers import auth_router
    from src.handlers.notes_handlers import note_router

    routers = (
        skill_router, progress_router, auth_router, note_router
    )

    for router in routers:
        app.include_router(router)