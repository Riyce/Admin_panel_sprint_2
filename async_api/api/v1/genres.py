from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from auth.permitions import JWTBearer
from models.filmwork import FilmworkBase
from models.genre import GenreBase, GenreDetail
from services.filmwork import FilmworkService, get_film_service
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get(
    "",
    response_model=list[GenreBase],
    summary="Genres list.",
    description="Genres list with pagination.",
    response_description="Name and id.",
    tags=["genre", "objects list"],
    dependencies=[Depends(JWTBearer(["list_genres"]))],
)
async def genre_list(
    page: Optional[int] = Query(default=1, alias="page[number]"),
    size: Optional[int] = Query(default=50, alias="page[size]"),
    genre_service: GenreService = Depends(get_genre_service),
) -> list[GenreBase]:
    return await genre_service.get_genres_list(page=page, size=size)


@router.get(
    "/{uuid}/",
    response_model=GenreDetail,
    summary="Get genre by ID.",
    description="Get genre by ID.",
    response_description="Name and id.",
    tags=["genre", "get by id"],
    dependencies=[Depends(JWTBearer(["list_genres"]))],
)
async def genre_info(
    uuid: UUID,
    genre_service: GenreService = Depends(get_genre_service),
) -> GenreDetail:
    genre_detail = await genre_service.get_genre(uuid=uuid)
    if not genre_detail:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre not found")
    return genre_detail


@router.get(
    "/{name}/film",
    response_model=list[FilmworkBase],
    summary="Get list of movies by genre name.",
    description="Get list of movies by genre name.",
    response_description="Movies name, rating and id.",
    tags=["genre", "film", "objects list"],
    dependencies=[Depends(JWTBearer(["search_genres"]))],
)
async def genre_popular_films(
    name: str,
    page: Optional[int] = Query(default=1, alias="page[number]"),
    size: Optional[int] = Query(default=50, alias="page[size]"),
    film_service: FilmworkService = Depends(get_film_service),
) -> list[FilmworkBase]:
    return await film_service.get_filmworks_list(page=page, size=size, filter_genre=name)
