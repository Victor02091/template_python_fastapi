from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    environment: Literal["local", "test", "dev", "preprod", "prod"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = (
        "INFO"
    )
    git_commit: str = "local-dev"

    oidc_authority: str
    oidc_client_id: str

    db_username: str = "local_user"
    db_password: str = "local_password"
    db_host: str = "db"
    db_port: str = "5432"
    db_name: str = "local_app"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def db_uri(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_username}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
