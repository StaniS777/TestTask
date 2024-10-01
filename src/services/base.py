from abc import ABC
from uuid import UUID
from typing import Any, TypeVar, Generic


from src.repositories.base import BaseRepository
from src.schemas.base import BaseModel


RepoT = TypeVar("RepoT", bound=BaseRepository)
RetrieveSchema = TypeVar("RetrieveSchema", bound=BaseModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class BaseService(Generic[RepoT, RetrieveSchema, CreateSchema, UpdateSchema], ABC):
    retrieve_schema: RetrieveSchema
    create_schema: CreateSchema
    update_schema: UpdateSchema

    def __init__(self, repo: RepoT):
        self.repo = repo

    async def get_one_by_id(self, obj_id: str | UUID) -> RetrieveSchema:
        instance = await self.repo.get_one_by_id(obj_id)
        result = self.retrieve_schema.model_validate(instance)
        return result

    async def get_one_by_field(self, field_name: str, value: str) -> RetrieveSchema:
        instance = await self.repo.get_one_by_field(field_name, value)
        result = self.retrieve_schema.model_validate(instance)
        return result

    async def get_all(self) -> list[RetrieveSchema]:
        instances = await self.repo.get_all()
        result = [
            self.retrieve_schema.model_validate(instance) for instance in instances
        ]
        return result

    async def create(self, data: CreateSchema) -> RetrieveSchema:
        instance = await self.repo.create_one(data.model_dump())
        result = self.retrieve_schema.model_validate(instance)
        return result

    async def update(
        self, obj_id: str | UUID, data: UpdateSchema, partial=True
    ) -> RetrieveSchema:
        instance = await self.repo.update_one(
            obj_id, data.model_dump(exclude_unset=partial)
        )
        result = self.retrieve_schema.model_validate(instance)
        return result

    async def delete(self, obj_id: str | UUID) -> UUID:
        deleted_pk = await self.repo.delete(obj_id)
        return deleted_pk

    async def get_list_by_ids(self, obj_ids: list[str | UUID]) -> list[RetrieveSchema]:
        instances = await self.repo.get_list_by_ids(obj_ids)
        result = [
            self.retrieve_schema.model_validate(instance) for instance in instances
        ]
        return result
