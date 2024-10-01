from pydantic import BaseModel as PydanticModel, ConfigDict


class BaseModel(PydanticModel):
    model_config = ConfigDict(from_attributes=True)


class StatusSchema(BaseModel):
    status: str = "ok"
