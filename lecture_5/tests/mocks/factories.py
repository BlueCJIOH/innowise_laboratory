from polyfactory.factories import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory

from book_api.api.v1.schemas import BookInSchema
from book_api.domain.commands import (
    CreateBookCommand,
    DeleteBookCommand,
    GetBookCommand,
    GetBookListCommand,
    PaginationQuery,
    UpdateBookCommand,
    BookSearchQuery,
)
from book_api.domain.entities import Book


class BookFactory(DataclassFactory[Book]):
    __model__ = Book


class BookInSchemaFactory(ModelFactory[BookInSchema]):
    __model__ = BookInSchema

    @classmethod
    def title(cls) -> str:
        return cls.__faker__.sentence(nb_words=3).rstrip(".")

    @classmethod
    def author(cls) -> str:
        return cls.__faker__.name()

    @classmethod
    def year(cls) -> int:
        return cls.__faker__.random_int(min=1900, max=2024)


class GetBookListCommandFactory(DataclassFactory[GetBookListCommand]):
    __model__ = GetBookListCommand


class GetBookCommandFactory(DataclassFactory[GetBookCommand]):
    __model__ = GetBookCommand


class CreateBookCommandFactory(DataclassFactory[CreateBookCommand]):
    __model__ = CreateBookCommand


class UpdateBookCommandFactory(DataclassFactory[UpdateBookCommand]):
    __model__ = UpdateBookCommand


class DeleteBookCommandFactory(DataclassFactory[DeleteBookCommand]):
    __model__ = DeleteBookCommand


class PaginationQueryFactory(DataclassFactory[PaginationQuery]):
    __model__ = PaginationQuery


class BookSearchQueryFactory(DataclassFactory[BookSearchQuery]):
    __model__ = BookSearchQuery
