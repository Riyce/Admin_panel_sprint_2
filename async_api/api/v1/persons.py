from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from auth.permitions import JWTBearer
from models.filmwork import FilmworkBase
from models.person import PersonDetail
from services.filmwork import FilmworkService, get_film_service
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get(
    "/{uuid}/",
    response_model=PersonDetail,
    summary="Get person by ID.",
    description="Get person by ID.",
    response_description="Detailed person information.",
    tags=["person", "get by id"],
    dependencies=[Depends(JWTBearer(["list_persons"]))],
)
async def person_info(
    uuid: UUID,
    person_service: PersonService = Depends(get_person_service),
) -> PersonDetail:
    person_detail = await person_service.get_person(uuid=uuid)
    if not person_detail:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")
    return person_detail


@router.get(
    "/{uuid}/film",
    response_model=list[FilmworkBase],
    summary="Get list of movies by person id.",
    description="Get list of movies by person id.",
    response_description="Movies name, rating and id.",
    tags=["person", "film", "objects list"],
    dependencies=[Depends(JWTBearer(["search_persons"]))],
)
async def films_with_person(
    uuid: UUID,
    page: Optional[int] = Query(default=1, alias="page[number]"),
    size: Optional[int] = Query(default=50, alias="page[size]"),
    film_service: FilmworkService = Depends(get_film_service),
) -> list[FilmworkBase]:
    return await film_service.get_filmworks_list(page=page, size=size, filter_actor=uuid)


@router.get(
    "/search",
    response_model=list[PersonDetail],
    summary="Persons list with search by name.",
    description="Persons list with search by name.",
    response_description="Person`s name, id, roles and mowies.",
    tags=["person", "objects list", "search"],
    dependencies=[Depends(JWTBearer(["search_persons"]))],
)
async def person_search(
    query: str,
    page: Optional[int] = Query(default=1, alias="page[number]"),
    size: Optional[int] = Query(default=50, alias="page[size]"),
    person_service: PersonService = Depends(get_person_service),
) -> list[PersonDetail]:
    res = await person_service.get_person_list(query=query, page=page, size=size)
    return res
