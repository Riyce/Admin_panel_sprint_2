from pydantic import BaseSettings, Field


class ETLSettings(BaseSettings):
    BATCH_SIZE: int = 10
    READ_TIMEOUT: int = 1000
    CLICKHOUSE_SERVER: str = "localhost"
    KAFKA_TOPIC: str = Field("views", env="MOVIE_PROGRESS_TOPIC")
    KAFKA_HOST: str = "localhost"
    KAFKA_PORT: int = 9092

    @property
    def kafka_uri(self) -> str:
        return f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"


settings = ETLSettings()
