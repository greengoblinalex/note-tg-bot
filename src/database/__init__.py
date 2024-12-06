from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from src.config import DATABASE_URL


engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def connection(func):
    async def wrapper(*args, **kwargs):
        session = kwargs.pop("session", None)
        if session is None:
            async with async_session() as session:
                return await func(session=session, *args, **kwargs)
        else:
            return await func(session=session, *args, **kwargs)
    return wrapper
