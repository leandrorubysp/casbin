import casbin
import sqlalchemy_adapter
from sqlalchemy import create_engine

from app.core.config import settings


def build_sync_db_uri() -> str:
    return (
        f"postgresql://{settings.POSTGRES_USER}:"
        f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
        f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )


_sync_engine = create_engine(build_sync_db_uri(), future=True)

_adapter = sqlalchemy_adapter.Adapter(
    _sync_engine,
    table_name=settings.CASBIN_DB_TABLE,
)

_enforcer: casbin.Enforcer | None = None


def get_enforcer() -> casbin.Enforcer:
    global _enforcer
    if _enforcer is None:
        _enforcer = casbin.Enforcer(settings.CASBIN_MODEL_PATH, _adapter)
        _enforcer.load_policy()
    return _enforcer