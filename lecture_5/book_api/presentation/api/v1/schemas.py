from typing import Any, Generic, TypeVar
from datetime import datetime

from pydantic import BaseModel, Field

from book_api.domain.entities import Book


TData = TypeVar("TData")
TListItem = TypeVar("TListItem")


class PaginationOutSchema(BaseModel):
    page: int
    limit: int
    total: int


class ListPaginatedResponse(BaseModel, Generic[TListItem]):
    items: list[TListItem]
    pagination: PaginationOutSchema


class ApiResponse(BaseModel, Generic[TData]):
    data: TData | dict | list = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[Any] = Field(default_factory=list)


class BookOutSchema(BaseModel):
    id: int
    title: str
    author: str
    year: int | None

    @staticmethod
    def from_entity(entity: Book) -> "BookOutSchema":
        return BookOutSchema(
            id=entity.id,
            title=entity.title,
            author=entity.author,
            year=entity.year,
        )


class BookInSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    year: int | None = Field(default_factory=lambda: datetime.now().year, gt=0, le=9999)


class BookUpdateSchema(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, min_length=1, max_length=255)
    year: int | None = Field(default=None, gt=0, le=9999)
