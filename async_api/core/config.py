import os
from logging import config as logging_config
from pathlib import Path

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

HOST_DEFAULT = "127.0.0.1"
PROJECT_NAME = os.getenv("PROJECT_NAME", "Async API movies service")

REDIS_HOST = os.getenv("REDIS_HOST", HOST_DEFAULT)
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REIDS_RECORD_LIVE_TIME = 60

ELASTIC_HOST = os.getenv("ELASTIC_HOST", HOST_DEFAULT)
ELASTIC_PORT = int(os.getenv("ELASTIC_PORT", 9200))

USER_CHECK_URL = f"{os.getenv('AUTH_HOST', HOST_DEFAULT)}/api/v1/auth/check/action"


BASE_DIR = Path(__file__).resolve().parent.parent
