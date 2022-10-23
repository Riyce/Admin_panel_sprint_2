from uuid import UUID

from pydantic import Field

from models.base import Base as BaseModel


class PersonBase(BaseModel):
    id: UUID = Field(..., alias="uuid")
    name: str = Field(..., alias="full_name")


class PersonDetail(PersonBase):
    roles: list[str]
    film_ids: list[UUID]
