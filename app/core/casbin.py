import casbin
import sqlalchemy_adapter

from app.core.config import settings

_enforcer: casbin.Enforcer | None = None


def get_casbin_enforcer() -> casbin.Enforcer:
    global _enforcer
    if _enforcer is None:
        db_url_sync = settings.DATABASE_URL.replace("+asyncpg", "")

        adapter = sqlalchemy_adapter.Adapter(
            db_url_sync,
            table_name=settings.CASBIN_TABLE_NAME,
            create_table=True,
        )

        _enforcer = casbin.Enforcer(settings.CASBIN_MODEL_PATH, adapter)
        _enforcer.load_policy()

    return _enforcer