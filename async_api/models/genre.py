from uuid import UUID

from pydantic import Field

from models.base import Base as BaseModel


class GenreBase(BaseModel):
    id: UUID = Field(..., alias="uuid")
    name: str


class GenreDetail(GenreBase):
    pass
