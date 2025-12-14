from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.api.schemas import Tenant, TenantCreate, TenantUpdate
from app.db.models import Tenant as TenantModel

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("", response_model=Tenant, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    tenant_in: TenantCreate,
    db: AsyncSession = Depends(get_db),
):
    tenant = TenantModel(name=tenant_in.name)
    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)
    return tenant


@router.get("", response_model=List[Tenant])
async def list_tenants(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TenantModel))
    tenants = result.scalars().all()
    return tenants


@router.get("/{tenant_id}", response_model=Tenant)
async def get_tenant(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TenantModel).where(TenantModel.id == tenant_id))
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    return tenant


@router.put("/{tenant_id}", response_model=Tenant)
async def update_tenant(
    tenant_id: int,
    tenant_in: TenantUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TenantModel).where(TenantModel.id == tenant_id))
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")

    if tenant_in.name is not None:
        tenant.name = tenant_in.name

    await db.commit()
    await db.refresh(tenant)
    return tenant


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TenantModel).where(TenantModel.id == tenant_id))
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")

    await db.delete(tenant)
    await db.commit()
    return None