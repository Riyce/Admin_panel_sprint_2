import json
import logging
import time

from elasticsearch import Elasticsearch

from config import (BASE_DIR, ELASTICSEARCH_HOST,
                    ELASTICSEARCH_INDEX_FILMWORK, ELASTICSEARCH_INDEX_GENRE,
                    ELASTICSEARCH_INDEX_PERSON, FILMWORK_QUERY_SIZE,
                    POSTGRESQL_CONFIG)
from etl import ETL
from utils import Entity

logger = logging.getLogger('ETL')


if __name__ == '__main__':
    sourses = [Entity.GENRE, Entity.FILMWORK, Entity.PERSON]
    size = FILMWORK_QUERY_SIZE
    indexes = [ELASTICSEARCH_INDEX_FILMWORK, ELASTICSEARCH_INDEX_GENRE, ELASTICSEARCH_INDEX_PERSON]
    es = Elasticsearch(hosts=[ELASTICSEARCH_HOST])
    etl = ETL(POSTGRESQL_CONFIG, es)
    connected = etl.check_connection()
    while not connected:
        logger.warning(f'No connection with Elasticsearch db. Check connection params and db.')
        time.sleep(5)
        connected = etl.check_connection()
    for index in indexes:
        if not es.indices.exists(index=index):
            logger.warning('Can`t connect to es index.')
            with open(BASE_DIR.joinpath(f'mappings/{index}_mapping.json')) as json_file:
                mapping = json.load(json_file)
            etl.init_db(index, mapping)
            logger.info(f'Index {index} created.')
            etl.run_etl(index, Entity.INIT, size)
            logger.info(f'Postgres data loaded')
    logger.info('ETL started.')
    while True:
        for index in indexes:
            if index == ELASTICSEARCH_INDEX_FILMWORK:
                for sourse in sourses:
                    logger.info(f'Check {sourse.value} table for index {index}.')
                    etl.run_etl(index, sourse, size)
                    time.sleep(5)
            elif index == ELASTICSEARCH_INDEX_PERSON:
                logger.info(f'Check {Entity.PERSON.value} table for index {index}.')
                etl.run_etl(index, Entity.PERSON, size)
                time.sleep(5)
            elif index == ELASTICSEARCH_INDEX_GENRE:
                logger.info(f'Check {Entity.GENRE.value} table for index {index}.')
                etl.run_etl(index, Entity.GENRE, size)
                time.sleep(5)
