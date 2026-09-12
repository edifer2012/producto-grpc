from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "producto-grpc"
    grpc_host: str = "0.0.0.0"
    grpc_port: int = Field(default=50051, ge=1, le=65535)
    grpc_max_workers: int = Field(default=10, ge=1, le=100)
    database_url: str = "postgresql+psycopg://producto:producto@localhost:5432/producto"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
