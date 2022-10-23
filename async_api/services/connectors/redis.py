from aioredis import Redis


class RedisConnector:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
