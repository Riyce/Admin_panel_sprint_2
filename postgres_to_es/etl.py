import json
import logging
from typing import Dict, Generator, Union

from elasticsearch import Elasticsearch

import queries
from backoff import backoff
from extractor import Extractor
from loader import Loader
from transformer import Transformer
from utils import Entity

logger = logging.getLogger('ETL')


class ETL:
    def __init__(self, dsn: Dict[str, Union[str, int]], es: Elasticsearch) -> None:
        self.dsn = dsn
        self.es = es

    def init_db(self, index: str, mapping: json) -> None:
        Loader(self.es).init_db(index, mapping)

    @backoff(logger)
    def check_connection(self):
        return self.es.ping()

    def run_etl(self, index: str, entity: Entity, query_size: int) -> None:  # filmwork
        exttractor_class = Extractor(self.dsn, index, entity, query_size)
        transformer_class = Transformer()
        loader = Loader(self.es)
        transformer = transformer_class.transform(index, loader.load(index))
        method = getattr(self, f'run_etl_{index}')
        try:
            method(exttractor_class, transformer, entity)
        except AttributeError:
            pass
        finally:
            exttractor_class.connection.close()

    @staticmethod
    def run_etl_movies(
            exttractor_class: Extractor,
            transformer: Generator,
            entity: Entity
    ) -> None:
        extractor = exttractor_class.extract(transformer, queries.FW_ETL_QUERY)
        if entity == Entity.GENRE:
            exttractor_class.extract_ids(extractor, queries.GENRE_QUERY, queries.GENRE_FILM_WORK_QUERY)
        elif entity == Entity.PERSON:
            exttractor_class.extract_ids(extractor, queries.PERSONS_QUERY, queries.PERSON_FILM_WORK_QUERY)
        elif entity == Entity.FILMWORK:
            exttractor_class.extract_ids(extractor, queries.FILM_WORK_QUERY)
        elif entity == Entity.INIT:
            exttractor_class.extract_ids(extractor, queries.ALL_FILM_WORK_QUERY)

    @staticmethod
    def run_etl_genres(
            exttractor_class: Extractor,
            transformer: Generator,
            entity: Entity
    ) -> None:
        extractor = exttractor_class.extract(transformer, queries.GENRE_ETL_QUERY)
        if entity == Entity.GENRE:
            exttractor_class.extract_ids(extractor, queries.GENRE_QUERY)
        elif entity == Entity.INIT:
            exttractor_class.extract_ids(extractor, queries.ALL_GENRE_QUERY)

    @staticmethod
    def run_etl_persons(
            exttractor_class: Extractor,
            transformer: Generator,
            entity: Entity
    ) -> None:
        extractor = exttractor_class.extract(transformer, queries.PERSON_ETL_QUERY)
        if entity == Entity.PERSON:
            exttractor_class.extract_ids(extractor, queries.PERSONS_QUERY)
        elif entity == Entity.INIT:
            exttractor_class.extract_ids(extractor, queries.ALL_PERSONS_QUERY)
