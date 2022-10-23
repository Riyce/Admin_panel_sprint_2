from typing import Dict, List

from elasticsearch import AsyncElasticsearch
from elasticsearch_dsl import Q, Search


class ElasticSearchConnector:
    DEFAULT_SIZE: int = 50
    DEFAULT_PAGE: int = 1

    def __init__(self, es: AsyncElasticsearch) -> None:
        self.es = es

    def __get_search(self, query_search_fields: List[str] = None, **kwargs) -> Search:
        search = Search()
        source = kwargs.get("source")
        if source:
            search = search.source(source)
        if "uuid" in kwargs:
            search = search.filter(
                "terms" if isinstance(kwargs["uuid"], list) else "term", id=kwargs["uuid"]
            ).extra(size=len(kwargs["uuid"]) if isinstance(kwargs["uuid"], list) else 1)
            return search
        page = kwargs.get("page") or self.DEFAULT_PAGE
        size = kwargs.get("size") or self.DEFAULT_SIZE
        sort = kwargs.get("sort")
        query = kwargs.get("query")
        filter_genre = kwargs.get("filter_genre")
        filter_actor = kwargs.get("filter_actor")
        filter_director = kwargs.get("filter_director")
        filter_writer = kwargs.get("filter_writer")
        from_ = (page - 1) * size
        search = search.extra(**{"from": from_, "size": size})
        if query:
            search = search.query("multi_match", query=query, fields=query_search_fields)
        if filter_genre:
            search = search.filter("term", genre=filter_genre)
        if filter_actor:
            search = search.query("nested", path="actors", query=Q("bool", filter=Q("term", actors__id=filter_actor)))
        if filter_director:
            search = search.query(
                "nested", path="directors", query=Q("bool", filter=Q("term", directors__id=filter_director))
            )
        if filter_writer:
            search = search.query(
                "nested", path="writers", query=Q("bool", filter=Q("term", writers__id=filter_writer))
            )
        if sort:
            search = search.sort(sort)
        return search

    async def execute(self, index: str, query_search_fields: List[str] = None, **kwargs) -> Dict:
        search = self.__get_search(query_search_fields, **kwargs).to_dict()
        result = await self.es.search(index=index, body=search)
        return result
