import asyncio

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal, engine, Base
from app.db.models import Tenant, User, Item


async def seed_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:  # type: AsyncSession
        tenant = Tenant(id=1, name="client1")
        u1 = User(id=1, email="admin@client1.local")
        u2 = User(id=2, email="manager@client1.local")
        u3 = User(id=3, email="support@client1.local")
        u4 = User(id=4, email="guest@client1.local")
        session.add_all([tenant, u1, u2, u3, u4])
        await session.flush()

        items = [
            Item(id=1, name="Item A", tenant_id=1, owner_user_id=1),
            Item(id=2, name="Item B", tenant_id=1, owner_user_id=2),
            Item(id=3, name="Item C", tenant_id=1, owner_user_id=3),
            Item(id=4, name="Item D", tenant_id=1, owner_user_id=4),
        ]
        session.add_all(items)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_db())