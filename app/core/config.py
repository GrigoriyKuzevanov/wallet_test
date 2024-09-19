from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    ECHO_SQL: bool

    @computed_field
    @property
    def asyncpg_url(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )

    TEST_DB_NAME: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    
    @computed_field
    @property
    def asyncpg_test_url(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.TEST_DB_HOST,
            port=self.TEST_DB_PORT,
            path=self.TEST_DB_NAME,    
        )
    
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, case_sensitive=True
    )


settings = Settings()
