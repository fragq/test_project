from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.core import settings


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = True,
        echo_pool: bool = False,
        max_overflow: int = 10,
        pool_size: int = 5,
    ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(
        self,
    ):
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=settings.db.SQLALCHEMY_DATABASE_URI,
    echo=settings.db.ECHO,
    echo_pool=settings.db.ECHO_POOL,
    max_overflow=settings.db.MAX_OVERFLOW,
    pool_size=settings.db.POOL_SIZE,
)

async def get_session_factory() -> AsyncSession:
    return db_helper.session_factory

SessionFactoryDep = Annotated[AsyncSession, Depends(get_session_factory)]

SessionDep = Annotated[AsyncSession, Depends(db_helper.session_getter)]
