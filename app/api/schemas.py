from pydantic import BaseModel


class TenantBase(BaseModel):
    name: str


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    name: str | None = None


class TenantInDBBase(TenantBase):
    id: int

    class Config:
        from_attributes = True


class Tenant(TenantInDBBase):
    pass


class UserBase(BaseModel):
    email: str
    full_name: str | None = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: str | None = None
    full_name: str | None = None


class UserInDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class ItemBase(BaseModel):
    id: int
    name: str
    tenant_id: int
    owner_user_id: int

    class Config:
        from_attributes = True


class ItemCreate(BaseModel):
    name: str
    tenant_id: int
    owner_user_id: int