from enum import Enum
from functools import wraps


class Entity(Enum):
    GENRE = 'GENRE'
    PERSON = 'PERSON'
    FILMWORK = 'FILMWORK'
    INIT = 'INIT'


def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        gen = func(*args, **kwargs)
        gen.send(None)
        return gen
    return inner
