from abc import ABC, abstractmethod
from book_api.domain.entities import Book


class IBookService(ABC):
    @abstractmethod
    def get_by_id(self, book_id: int) -> Book:
        raise NotImplementedError

    @abstractmethod
    def create(self, title: str, author: str, year: int | None) -> Book:
        raise NotImplementedError

    @abstractmethod
    def update(self, book_id: int, *, title: str | None, author: str | None, year: int | None) -> Book:
        raise NotImplementedError

    @abstractmethod
    def delete(self, book_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_many(
        self,
        *,
        offset: int,
        limit: int,
        title: str | None = None,
        author: str | None = None,
        year: int | None = None,
    ) -> list[Book]:
        raise NotImplementedError

    @abstractmethod
    def count_many(self, *, title: str | None = None, author: str | None = None, year: int | None = None) -> int:
        raise NotImplementedError
