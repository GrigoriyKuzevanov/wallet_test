from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str

    @computed_field
    @property
    def asyncpg_url(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            path=self.DB_NAME,
        )

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, case_sensitive=True
    )


settings = Settings()
