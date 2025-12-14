from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_db,
    get_current_user,
    authorize_read_item,
    get_current_roles_for_tenant,
    authorize_create_item,
)
from app.api.schemas import ItemBase, ItemCreate
from app.db.models import Item, User

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{item_id}", response_model=ItemBase)
async def read_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    await authorize_read_item(item=item, current_user=current_user)
    return item


@router.get("", response_model=List[ItemBase])
async def list_items(
    tenant_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    roles = get_current_roles_for_tenant(current_user.id, tenant_id)

    if "admin" in roles or "manager" in roles:
        stmt = select(Item).where(Item.tenant_id == tenant_id)
    elif "support" in roles or "guest" in roles:
        stmt = select(Item).where(
            Item.tenant_id == tenant_id,
            Item.owner_user_id == current_user.id,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No role for this tenant",
        )

    result = await db.execute(stmt)
    items = result.scalars().all()
    return items


@router.post("", response_model=ItemBase, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: ItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _=Depends(lambda: None),  # placeholder, overridden below
):
    # Manually call authorize_create_item because we need tenant_id from body
    await authorize_create_item(tenant_id=item_in.tenant_id, current_user=current_user)

    item = Item(
        name=item_in.name,
        tenant_id=item_in.tenant_id,
        owner_user_id=item_in.owner_user_id,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item