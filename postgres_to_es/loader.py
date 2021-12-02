import json
import logging
from typing import Generator, List

import elasticsearch.exceptions
from elasticsearch import Elasticsearch

from backoff import backoff
from models.filmvork import Filmwork
from utils import coroutine

logger = logging.getLogger('Elasticsearch')


class Loader:

    def __init__(self, es: Elasticsearch, batch_size: int = 10) -> None:
        self.batch_size = batch_size
        self.es = es

    def init_db(self, index: str, mapping: json) -> None:
        try:
            self.es.indices.create(index=index, body=mapping)
        except elasticsearch.exceptions.RequestError:
            logger.warning(f'Index with name {index} already exists.')

    def prepare_query(self, index: str, load_data: List[Filmwork]) -> Generator:
        for num in range(0, len(load_data), self.batch_size):
            query = []
            for obj_ in load_data[num:num+self.batch_size]:
                query.append(
                    json.dumps(
                        {'index': {'_index': index, '_id': obj_.id}}
                    ) + '\n' + json.dumps(obj_.to_dict())
                )
            yield query

    @backoff(logger)
    @coroutine
    def load(self, index: str) -> Generator:
        while load_data := (yield):
            for query in self.prepare_query(index, load_data):
                self.es.bulk(body='\n'.join(query))
                logger.info(f'Loaded/updated {len(query)} to index {index}.')
