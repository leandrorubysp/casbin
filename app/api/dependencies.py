from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.db.models import User, Item
from app.core.casbin import get_enforcer


async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(db=Depends(get_db)) -> User:
    result = await db.execute(select(User).where(User.id == 1))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def authorize_read_item(
    item: Item,
    current_user: User = Depends(get_current_user),
):
    enforcer = get_enforcer()

    sub = str(current_user.id)
    dom = str(item.tenant_id)
    obj = "item"
    act = "read"
    sub_user_id = str(current_user.id)
    resource_user_id = str(item.owner_user_id)
    resource_tenant_id = str(item.tenant_id)

    allowed = enforcer.enforce(
        sub,
        dom,
        obj,
        act,
        sub_user_id,
        resource_user_id,
        resource_tenant_id,
    )
    if not allowed:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return True


def get_current_roles_for_tenant(user_id: int, tenant_id: int) -> list[str]:
    e = get_enforcer()
    tenant_str = str(tenant_id)
    roles = []
    for role in ["admin", "manager", "support", "guest"]:
        if e.has_role_for_user_in_domain(str(user_id), role, tenant_str):
            roles.append(role)
    return roles


async def authorize_create_item(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
):
    roles = get_current_roles_for_tenant(current_user.id, tenant_id)
    if "admin" not in roles and "manager" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin/manager can create items for this tenant",
        )
    return True