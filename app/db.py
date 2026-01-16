from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.settings import settings

api_engine = create_async_engine(url=settings.DATABASE_URL, echo=True)
api_session_local = async_sessionmaker(api_engine, class_=AsyncSession, expire_on_commit=False)

data_sync_engine = create_async_engine(settings.DATABASE_URL, echo=True)
data_sync_session_local = async_sessionmaker(api_engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with api_session_local(bind=api_engine) as session:
        yield session
