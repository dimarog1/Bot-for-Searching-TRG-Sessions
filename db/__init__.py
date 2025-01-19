from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from db.models.user import Base


async def init_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_session_factory():
    db = "postgres"
    user = "admin"
    password = "admin"
    host = "postgres"
    # host = "localhost"
    port = 5432
    # port = 6432
    DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

    engine = create_async_engine(DATABASE_URL, echo=True)

    return sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
