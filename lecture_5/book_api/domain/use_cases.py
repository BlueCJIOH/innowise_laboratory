from dataclasses import dataclass
from typing import List, Tuple

from book_api.domain.commands import (
    CreateBookCommand,
    DeleteBookCommand,
    GetBookCommand,
    GetBookListCommand,
    UpdateBookCommand,
)
from book_api.domain.entities import Book
from book_api.domain.services import IBookService


@dataclass
class BaseUseCase:
    def execute(self, *args, **kwargs):
        raise NotImplementedError


@dataclass
class GetBookListUseCase(BaseUseCase):
    book_service: IBookService

    def execute(self, command: GetBookListCommand) -> Tuple[List[Book], int]:
        books = self.book_service.find_many(
            offset=command.pagination.offset,
            limit=command.pagination.limit,
            title=command.search.title,
            author=command.search.author,
            year=command.search.year,
        )
        total = self.book_service.count_many(
            title=command.search.title,
            author=command.search.author,
            year=command.search.year,
        )
        return books, total


@dataclass
class GetBookUseCase(BaseUseCase):
    book_service: IBookService

    def execute(self, command: GetBookCommand) -> Book:
        return self.book_service.get_by_id(command.book_id)


@dataclass
class CreateBookUseCase(BaseUseCase):
    book_service: IBookService

    def execute(self, command: CreateBookCommand) -> Book:
        return self.book_service.create(command.title, command.author, command.year)


@dataclass
class UpdateBookUseCase(BaseUseCase):
    book_service: IBookService

    def execute(self, command: UpdateBookCommand) -> Book:
        return self.book_service.update(
            command.book_id,
            title=command.title,
            author=command.author,
            year=command.year,
        )


@dataclass
class DeleteBookUseCase(BaseUseCase):
    book_service: IBookService

    def execute(self, command: DeleteBookCommand) -> None:
        return self.book_service.delete(command.book_id)