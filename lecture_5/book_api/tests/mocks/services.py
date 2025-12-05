import random

from book_api.domain.entities import Book
from book_api.domain.services import IBookService
from book_api.tests.mocks.factories import BookFactory


class DummyBookService(IBookService):
    def get_by_id(self, book_id: int) -> Book:
        return BookFactory.build(id=book_id)

    def create(self, title: str, author: str, year: int | None) -> Book:
        return BookFactory.build(id=random.randint(1, 1000), title=title, author=author, year=year)

    def update(self, book_id: int, *, title: str | None, author: str | None, year: int | None) -> Book:
        return BookFactory.build(id=book_id, title=title or "title", author=author or "author", year=year)

    def delete(self, book_id: int) -> None:
        return None

    def find_many(self, *, offset: int, limit: int, title: str | None = None, author: str | None = None, year: int | None = None) -> list[Book]:
        return [BookFactory.build(id=i) for i in range(limit)]

    def count_many(self, *, title: str | None = None, author: str | None = None, year: int | None = None) -> int:
        return random.randint(0, 100)
