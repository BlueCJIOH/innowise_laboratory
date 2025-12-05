from pydantic import model_validator
from pydantic_settings import BaseSettings


class SQLiteSettings(BaseSettings):
    SQLITE_FILE_PATH: str = "book_api.db"
    SQLITE_URL: str | None = None

    @model_validator(mode="before") # noqa
    @classmethod
    def assemble_sqlite_url(cls, values: dict) -> dict:
        if values.get("SQLITE_URL"):
            return values

        file_path = values.get("SQLITE_FILE_PATH", "book_api.db")
        values["SQLITE_URL"] = f"sqlite:///{file_path}"
        return values

    @property
    def sqlite_url(self) -> str:
        return self.SQLITE_URL
