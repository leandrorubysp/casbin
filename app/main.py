import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.api.routes import items, tenants, users
from app.db.session import engine, Base


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    app.include_router(items.router, prefix=settings.API_V1_STR)
    app.include_router(tenants.router, prefix=settings.API_V1_STR)
    app.include_router(users.router, prefix=settings.API_V1_STR)

    @app.on_event("startup")
    async def on_startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)