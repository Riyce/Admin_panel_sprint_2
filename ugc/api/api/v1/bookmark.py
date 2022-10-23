from typing import List

from fastapi import APIRouter, Depends, Security, status
from models.bookmark import Bookmark, BookmarkBase, BookmarkFull
from services.bookmarks import BookmarkService, get_bookmark_service
from users.security import get_user

router = APIRouter(tags=["Bookmark"])


@router.post(
    "/bookmarks",
    summary="Add bookmark for movie.",
    description="Add bookmark to user`s bookmarks for movie with ID movie_id.",
    status_code=status.HTTP_201_CREATED,
)
async def add_bookmark(
    bookmark: BookmarkBase,
    event_sender: BookmarkService = Depends(get_bookmark_service),
    user_id: str = Security(get_user),
) -> None:
    review_full = Bookmark.get_object(bookmark, user_id)
    await event_sender.add_bookmark(review_full)


@router.delete(
    "/bookmarks/{bookmark_id}",
    summary="Delete user`s bookmark.",
    description="Delete bookmark from user`s bookmarks by bookmark_id.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bookmark(
    bookmark_id: str,
    event_sender: BookmarkService = Depends(get_bookmark_service),
    user_id: str = Security(get_user),
) -> None:
    await event_sender.delete_bookmark(bookmark_id, user_id)


@router.get(
    "/bookmarks",
    summary="Get user`s bookmarks.",
    description="Get all user`s bookmarks with pagination.",
    response_model=List[BookmarkFull],
    status_code=status.HTTP_200_OK,
)
async def get_bookmarks(
    first: int = 10,
    limit: int = 0,
    event_sender: BookmarkService = Depends(get_bookmark_service),
    user_id: str = Security(get_user),
) -> List[BookmarkFull]:
    return await event_sender.get_bookmarks(first, limit, user_id)
