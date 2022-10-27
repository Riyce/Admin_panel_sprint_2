import functools
import pickle
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Tuple

from db import redis


class Cacher(ABC):
    @abstractmethod
    def form_key(self, args: Tuple[Any], kwargs: Dict[str, Any]) -> str:
        """Forms a key value which is used for cached request"""

    @abstractmethod
    def is_cached(self, key: str) -> bool:
        """Checks if the request is already cached"""

    @abstractmethod
    def get_data(self, key: str) -> Any:
        """Retrieves data by key"""

    @abstractmethod
    def write_data(self, key: str, data: Any) -> None:
        """Caches data"""

    def __call__(self, func: Callable) -> Any:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            key = self.form_key(args=args, kwargs=kwargs)
            if self.is_cached(key):
                return self.get_data(key)
            else:
                result = func(*args, **kwargs)
                self.write_data(key, result)
                return result

        return wrapper


class redis_cache(Cacher):
    """
    Class for caching function calls with redis in async regime
    It's intended to use as decorator

    Usage:
        @redis_cache(namespace='some_namespace', ttl=0)
        def foo(*args, **kwargs):
            ...
    """

    def __init__(self, namespace: str, ttl: int = 0):
        self.namespace = namespace
        self.ttl = ttl

    def form_key(self, args: Tuple[Any], kwargs: Dict[str, str]) -> str:
        payload = {**{i: arg for i, arg in enumerate(args)}, **kwargs}
        redis_key = "::".join([f"{key}:{value}" for key, value in payload.items() if value])
        return f"{self.namespace}-{redis_key}"

    async def is_cached(self, key: str) -> bool:
        return await redis.redis.exists(key)

    async def get_data(self, key: str) -> Any:
        value = await redis.redis.get(key=key)
        return pickle.loads(value)

    async def write_data(self, key: str, data: Any) -> None:
        await redis.redis.set(key=key, value=pickle.dumps(data), expire=self.ttl)

    def __call__(self, func: Callable) -> Any:
        async def helper(func, *args, **kwargs):
            return await func(*args, **kwargs)

        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            key = self.form_key(args, kwargs)
            if await self.is_cached(key):
                return await self.get_data(key)
            else:
                result = await helper(func, *args, **kwargs)
                await self.write_data(key, result)
                return result

        return wrapper
