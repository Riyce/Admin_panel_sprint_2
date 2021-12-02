import logging.config
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATE_DIR = BASE_DIR.joinpath('states')


POSTGRESQL_CONFIG = {
    'dbname': os.environ.get('POSTGRES_DB'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': os.environ.get('POSTGRES_HOST'),
    'port': os.environ.get('POSTGRES_PORT')
}
ELASTICSEARCH_HOST = os.environ.get("ES_HOST")
ELASTICSEARCH_INDEX_FILMWORK = 'movies'
ELASTICSEARCH_INDEX_GENRE = 'genres'
ELASTICSEARCH_INDEX_PERSON = 'persons'
FILMWORK_QUERY_SIZE = 20

LOGGING = {
    'version': 1,
    'handlers': {
        'postgreFileHandler': {
            'class': 'logging.FileHandler',
            'formatter': 'formatter',
            'filename': BASE_DIR.joinpath('logs/postgresql.log')
        },
        'elasticsearchFileHandler': {
            'class': 'logging.FileHandler',
            'formatter': 'formatter',
            'filename': BASE_DIR.joinpath('logs/elasticsearch.log')
        },
        'etlFileHandler': {
            'class': 'logging.FileHandler',
            'formatter': 'formatter',
            'filename': BASE_DIR.joinpath('logs/etl.log')
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'PostgreSQL': {
            'handlers': ['postgreFileHandler', 'console'],
            'level': 'INFO',
        },
        'Elasticsearch': {
            'handlers': ['elasticsearchFileHandler', 'console'],
            'level': 'INFO',
        },
        'ETL': {
            'handlers': ['etlFileHandler', 'console'],
            'level': 'INFO',
        }
    },
    'formatters': {
        'formatter': {
            'format': '%(asctime)s | %(levelname)s - %(message)s'
        }
    }
}
logging.config.dictConfig(LOGGING)
