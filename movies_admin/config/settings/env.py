from pathlib import Path

import environ

FILE = Path(__file__).resolve().parent.parent.joinpath('.env')
env = environ.Env(
    ALLOWED_HOSTS=(list, ['127.0.0.1', 'localhost']),
    SECRET_KEY=(str, 'qwerty'),
    DATABASE_URL=(str, 'sqlite:///db.sqlite'),
)

with open(FILE) as file:
    environ.Env.read_env(file)