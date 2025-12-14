from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, casbin_enforce

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    dependencies=[Depends(casbin_enforce(obj="users", act="read"))],
)
async def list_users(db: AsyncSession = Depends(get_db)):
    # placeholder: return empty list
    return []