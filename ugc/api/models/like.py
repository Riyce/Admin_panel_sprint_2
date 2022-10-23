from models.mixins import CreeateMixin
from pydantic.fields import Field
from pydantic.main import BaseModel


class MovieLikeBase(BaseModel):
    movie_id: str
    score: int = Field(ge=1, le=10)


class ReviewLikeBase(BaseModel):
    review_id: str
    score: int = Field(ge=1, le=10)


class MovieLike(MovieLikeBase, CreeateMixin):
    user_id: str


class ReviewLike(ReviewLikeBase, CreeateMixin):
    user_id: str
