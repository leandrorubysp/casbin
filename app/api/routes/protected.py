from fastapi import APIRouter, Depends

from app.api.deps import casbin_enforce

router = APIRouter(prefix="/protected", tags=["protected"])


@router.get(
    "/data1",
    dependencies=[Depends(casbin_enforce(obj="data1", act="read"))],
)
async def read_data1():
    return {"message": "You are allowed to read data1"}