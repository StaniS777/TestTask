from abc import ABC
from typing import Any, TypeVar, Generic
from uuid import UUID

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import Base


ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT], ABC):
    model: ModelT

    def __init__(self, session: AsyncSession):
        self._session = session

    @property
    def default_select_query(self):
        stmt = select(self.model)
        return stmt

    async def get_all(self) -> list[ModelT]:
        stmt = self.default_select_query
        query_result = await self._session.execute(stmt)
        result = query_result.scalars().all()
        return result

    async def get_one_by_id(self, obj_id: str | UUID) -> ModelT:
        stmt = self.default_select_query.where(self.model.pk == obj_id)
        query_result = await self._session.execute(stmt)
        result = query_result.scalar_one()
        return result

    async def get_one_by_field(self, field_name: str, value: Any) -> ModelT:
        stmt = self.default_select_query.where(getattr(self.model, field_name) == value)
        query_result = await self._session.execute(stmt)
        result = query_result.scalar_one()
        return result

    async def create_one(self, data: dict[str, Any] = None, **kwargs) -> ModelT:
        if data is None:
            data = {}
        data.update(kwargs)
        stmt = insert(self.model).values(**data).returning(self.model)
        query_result = await self._session.execute(stmt)
        result = query_result.scalar_one()
        return result

    async def update_one(
        self, obj_id: str | UUID, data: dict[str, Any] = None, **kwargs
    ) -> ModelT:
        if data is None:
            data = {}
        data.update(kwargs)
        stmt = (
            update(self.model)
            .where(self.model.pk == obj_id)
            .values(**data)
            .returning(self.model)
        )
        query_result = await self._session.execute(stmt)
        result = query_result.scalar_one()
        return result

    async def delete(self, obj_id: str | UUID) -> UUID:
        stmt = (
            delete(self.model).where(self.model.pk == obj_id).returning(self.model.pk)
        )
        query_result = await self._session.execute(stmt)
        result = query_result.scalar_one()
        return result

    async def get_list_by_ids(self, obj_ids: list[str | UUID]) -> list[ModelT]:
        stmt = self.default_select_query.where(self.model.pk.in_(obj_ids))
        query_result = await self._session.execute(stmt)
        result = query_result.scalars().all()
        return result
