from fastapi import APIRouter, Depends, Security, status
from models.progress import MovieProgress, MovieProgressBase
from services.progress import ProgressService, get_progress_service
from users.security import get_user

router = APIRouter(tags=["Events"])


@router.post(
    "/progress",
    summary="Add movie progress.",
    description="Add user`s movie progress for movie with ID movie_id. "
    "Total time is full movie time. "
    "Time is current movie time",
    status_code=status.HTTP_201_CREATED,
)
async def send_view_progress(
    movie_progress: MovieProgressBase,
    event_sender: ProgressService = Depends(get_progress_service),
    user_id: str = Security(get_user),
) -> None:
    user_movie_progress = MovieProgress.get_object(movie_progress, user_id)
    await event_sender.send_movie_progress(user_movie_progress)


@router.post(
    "/online",
    summary="Add movie online.",
    description="Add movie to online list.",
    status_code=status.HTTP_201_CREATED,
)
async def send_view_progress(
    movie_progress: MovieProgressBase,
    event_sender: ProgressService = Depends(get_progress_service),
    user_id: str = Security(get_user),
) -> None:
    user_movie_progress = MovieProgress.get_object(movie_progress, user_id)
    await event_sender.send_movie_online(user_movie_progress)
