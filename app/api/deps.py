from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_maker
from app.core.casbin import get_casbin_enforcer
from app.core.config import settings


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


def get_current_user(username: str = "alice"):
    return username


def casbin_enforce(
    obj: str,
    act: str,
):
    def dependency(
        current_user: str = Depends(get_current_user),
    ):
        e = get_casbin_enforcer()
        if not e.enforce(current_user, obj, act):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return True

    return dependency