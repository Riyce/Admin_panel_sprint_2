from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).parent.resolve()


class PostgresDNS(BaseSettings):
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5433
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "auth"

    @property
    def url(self) -> str:
        return (
            "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
            "{POSTGRES_HOST}/{POSTGRES_DB}".format_map(self.dict())
        )


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    DEBUG: bool = True
    JWT_SECRET_KEY: str = "super-secret"
    SECRET_KEY: str = "extra secret"
    PASSWORD_SALT: str = "extra salt"
    HASH_ALGORITHM: str = "sha256"
    ACCESS_TOKEN_TTL: int = 5 * 60 * 60
    JWT_ACCESS_TOKEN_EXPIRES: int = 15 * 60
    REFRESH_TOKEN_TTL: int = 60 * 60 * 24 * 15
    JWT_REFRESH_TOKEN_EXPIRES: int = 60 * 60 * 24 * 15
    REDIS_PREFIX: str = "auth"
    YANDEX_CLIENT_ID: str = "925a2a14c8a54953b6bc2e92433d33bc"
    YANDEX_CLIENT_SECRET: str = "dc28bcd4f66945af87d167669917ef6a"
    YANDEX_REDIRECT_URL: str = "http://127.0.0.1:8000/v1/oauth/callback/yandex"
    DAYS_LIMIT: str = "200 per day"
    HOURS_LIMIT: str = "10 per hour"
    JAEGER_HOST: str = "127.0.0.1"
    JAEGER_PORT: int = 6831
    VK_APP_ID: int = 8226576
    VK_APP_SECURE_KEY: str = "uuhYbEzcel7Pg736mzXz"

    @property
    def redis_uri(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def limits(self) -> list[str]:
        return [self.DAYS_LIMIT, self.HOURS_LIMIT]


settings = Settings()
postgres_settings = PostgresDNS()
