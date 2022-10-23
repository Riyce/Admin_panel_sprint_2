from models.mixins import CreeateMixin
from pydantic.main import BaseModel


class MovieProgressBase(BaseModel):
    movie_id: str
    time: int
    total_time: int


class MovieProgress(MovieProgressBase, CreeateMixin):
    user_id: str

    def get_movie_user(self) -> dict[str, str]:
        return {
            "movie": self.movie_id,
            "user": self.user_id
        }
