from book_api.core.configs.database import SQLiteSettings


class Settings(
    SQLiteSettings
):
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()