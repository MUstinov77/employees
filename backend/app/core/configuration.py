from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    TITLE: str = "EmployeesApi"
    MAX_PHOTO_SIZE_KB: int
    DB_USER: str
    DB_PASSWORD: str
    PHOTO_DIRECTORY_PATH: str = f"{Path(__file__).parents[2]}/photos/"
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def DB_URI(self): # noqa
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[2].joinpath(".env")
    )


def get_settings() -> Settings:
    return Settings()


settings = Settings()