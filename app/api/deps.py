from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import async_session_maker, current_tenant_id
from app.core.casbin import get_casbin_enforcer
from app.core.config import settings
from app.models.user import User, Tenant


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def get_current_tenant_id(
    db: AsyncSession = Depends(get_db),
    x_tenant_id: int | None = Header(default=None, alias="X-Tenant-ID"),
) -> int:
    """
    Resolve current tenant from X-Tenant-ID header and store it in ContextVar.
    """
    if x_tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Tenant-ID header required",
        )

    result = await db.execute(select(Tenant).where(Tenant.id == x_tenant_id))
    tenant = result.scalar_one_or_none()
    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    current_tenant_id.set(tenant.id)
    return tenant.id


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_current_tenant_id),
) -> User:
    """
    For now, just return a hardcoded user per tenant.
    In a real app, you would use auth and query User by token.
    """
    # Example: assume 'alice' belongs to this tenant.
    result = await db.execute(
        select(User).where(User.username == "alice", User.tenant_id == tenant_id)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found in this tenant",
        )
    return user


def casbin_enforce(
    obj: str,
    act: str,
):
    def dependency(
        current_user: User = Depends(get_current_user),
        tenant_id: int = Depends(get_current_tenant_id),
    ):
        e = get_casbin_enforcer()
        # We'll use 'dom' (domain) in Casbin model to represent the tenant.
        if not e.enforce(current_user.username, str(tenant_id), obj, act):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return True

    return dependency