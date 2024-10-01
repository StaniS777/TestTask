from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from sqlalchemy import exc

from src.config import settings


engine = create_async_engine(settings.database_url)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = async_sessionmaker(engine)
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise error
