from dataclasses import dataclass

from book_api.domain.errors import BookNotFound
from book_api.domain.entities import Book
from book_api.domain.services import IBookService
from book_api.gateways.sqlite.repositories import IBookRepository
from book_api.helpers.errors import fail


@dataclass
class BookService(IBookService):
    repository: IBookRepository

    def get_by_id(self, book_id: int) -> Book:
        return self.repository.get_by_id(book_id) or fail(BookNotFound())

    def create(self, title: str, author: str, year: int | None) -> Book:
        return self.repository.create(title=title, author=author, year=year)

    def update(self, book_id: int, *, title: str | None, author: str | None, year: int | None) -> Book:
        return self.repository.update(book_id, title=title, author=author, year=year) or fail(BookNotFound())

    def delete(self, book_id: int) -> None:
        self.repository.delete(book_id) or fail(BookNotFound())

    def find_many(
        self, *,
        offset: int,
        limit: int,
        title: str | None = None,
        author: str | None = None,
        year: int | None = None
    ) -> list[Book]:
        return self.repository.find_many(title=title, author=author, year=year, offset=offset, limit=limit)

    def count_many(self, *, title: str | None = None, author: str | None = None, year: int | None = None) -> int:
        return self.repository.count_many(title=title, author=author, year=year)
