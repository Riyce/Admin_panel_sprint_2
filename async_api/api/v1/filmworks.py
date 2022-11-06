from http import HTTPStatus
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from models.filmwork import FilmworkBase, FilmworkDetail, FilmworkName
from services.auth import get_current_user
from services.filmwork import FilmworkService, get_film_service


router = APIRouter()


@router.get(
    "/{uuid}/",
    response_model=FilmworkDetail,
    summary="Get movie by ID.",
    description="Get movie by ID.",
    response_description="Detailed movie information.",
    tags=["film", "get by id"],
)
async def film_details(
        uuid: str,
        film_service: FilmworkService = Depends(get_film_service),
        user: Any = Depends(get_current_user)
) -> FilmworkDetail:
    filmwork = await film_service.get_filmwork(uuid)
    if not filmwork:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film not found")
    return filmwork


@router.get(
    "",
    response_model=list[FilmworkBase],
    summary="Movies list.",
    description="Movies list with pagination, sort and actors, writers, directors and genres filters.",
    response_description="Movies name, rating and id.",
    tags=["film", "objects list"],
)
async def film_list(
    sort: Optional[str] = None,
    page: Optional[int] = Query(default=1, alias="page[number]"),
    size: Optional[int] = Query(default=50, alias="page[size]"),
    exclude: Optional[str] = Query(default=None, alias="exclude"),
    filter_genre: Optional[str] = Query(default=None, alias="filter[genre]"),
    filter_actor: Optional[str] = Query(default=None, alias="filter[actor]"),
    filter_director: Optional[str] = Query(default=None, alias="filter[director]"),
    filter_writer: Optional[str] = Query(default=None, alias="filter[writer]"),
    film_service: FilmworkService = Depends(get_film_service),
) -> list[FilmworkBase]:
    filmworks = await film_service.get_filmworks_list(
        sort=sort,
        page=page,
        size=size,
        filter_genre=filter_genre,
        filter_actor=filter_actor,
        filter_director=filter_director,
        filter_writer=filter_writer,
        exclude=exclude
    )
    return filmworks


@router.get(
    "/search",
    response_model=list[FilmworkBase],
    summary="Movies list with search params.",
    description="Movies list with pagination, sort and search param.",
    response_description="Movies name, rating and id.",
    tags=["film", "objects list", "search"],
)
async def film_search(
    query: str,
    sort: Optional[str] = None,
    page: Optional[int] = Query(default=1, alias="page[number]"),
    size: Optional[int] = Query(default=50, alias="page[size]"),
    film_service: FilmworkService = Depends(get_film_service),
) -> list[FilmworkBase]:
    filmworks = await film_service.get_filmworks_list(sort=sort, query=query, page=page, size=size)
    return filmworks


@router.get(
    "/names",
    response_model=list[FilmworkBase],
    summary="Movies list with names.",
    description="Movies names list.",
    response_description="Movies name.",
    tags=["film", "objects list"],
)
async def film_names(
    ids: str,
    film_service: FilmworkService = Depends(get_film_service),
) -> list[FilmworkBase]:
    filmworks = await film_service.get_filmworks_list(uuid=ids.split(","))
    return filmworks
