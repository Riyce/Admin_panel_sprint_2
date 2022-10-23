import multiprocessing
import os

from core.logger import LOGGING

workers_per_core_str = os.getenv("WEBAPP_WORKERS_PER_CORE", "1")
host = os.getenv("WEBAPP_HOST", "0.0.0.0")
port = os.getenv("WEBAPP_PORT", "8000")
use_loglevel = os.getenv("WEBAPP_LOG_LEVEL", "info")

cores = multiprocessing.cpu_count()
default_web_concurrency = int(workers_per_core_str) * cores
web_concurrency = max(int(default_web_concurrency), 2)

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = f"{host}:{port}"
keepalive = 120
logconfig_dict = LOGGING
