from abc import ABC, abstractmethod
from typing import Type, TypeVar

from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class GenericRepository[T](ABC):

    @abstractmethod
    async def get(self, **filters) -> T | None: ...

    @abstractmethod
    async def update(self, data: dict, **filters) -> T | None: ...


class GenericSQLAlchemyRepository(GenericRepository[T], ABC):

    def __init__(self, session: AsyncSession, model: Type[T]):
        self._session = session
        self._model = model

    def _build_where_clause(self, **filters):
        where_clause = []
        for c, v in filters.items():
            if not hasattr(self._model, c):
                raise ValueError(f"Invalid column name {c}")
            where_clause.append(getattr(self._model, c) == v)
        return where_clause

    async def get(self, **filters) -> T | None:
        where_clause = self._build_where_clause(**filters)
        item = await self._session.scalar(
            select(self._model).where(and_(*where_clause))
        )
        return item

    async def update(self, data: dict, **filters) -> T | None:
        where_clause = self._build_where_clause(**filters)
        item = await self._session.scalar(
            update(self._model)
            .where(and_(*where_clause))
            .values(data)
            .returning(self._model)
        )
        return item
