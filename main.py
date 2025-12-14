from fastapi import FastAPI

from app.core.config import settings
from app.api.routes import users, protected
from app.core.casbin import get_casbin_enforcer


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    @app.on_event("startup")
    async def startup_event():
        _ = get_casbin_enforcer()

    app.include_router(users.router)
    app.include_router(protected.router)

    return app


app = create_app()