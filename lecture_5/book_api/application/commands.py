from dataclasses import dataclass, field


@dataclass
class PaginationQuery:
    page: int = 0
    limit: int = 10

    @property
    def offset(self) -> int:
        return self.page * self.limit


@dataclass
class BookSearchQuery:
    title: str | None = None
    author: str | None = None
    year: int | None = None


@dataclass
class GetBookListCommand:
    search: BookSearchQuery = field(default_factory=BookSearchQuery)
    pagination: PaginationQuery = field(default_factory=PaginationQuery)


@dataclass
class GetBookCommand:
    book_id: int


@dataclass
class CreateBookCommand:
    title: str
    author: str
    year: int | None = None


@dataclass
class UpdateBookCommand:
    book_id: int
    title: str | None = None
    author: str | None = None
    year: int | None = None


@dataclass
class DeleteBookCommand:
    book_id: int
