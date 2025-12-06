from pydantic_settings import SettingsConfigDict

from book_api.core.configs.database import SQLiteSettings


class Settings(SQLiteSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()
