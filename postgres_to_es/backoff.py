from functools import wraps
from logging import Logger
from time import sleep


def backoff(
        logger: Logger,
        start_sleep_time: int = 1,
        factor: int = 2,
        border_sleep_time: int = 60
):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            attempt = 1
            delay = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f'Try: {attempt} \n {e}')
                    sleep(delay)
                    attempt += 1
                    new_time = start_sleep_time * factor
                    delay = new_time if new_time < border_sleep_time else border_sleep_time
        return inner
    return func_wrapper
