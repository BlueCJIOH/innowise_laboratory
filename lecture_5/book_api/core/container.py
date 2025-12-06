from functools import lru_cache

import punq

from book_api.domain.services import IBookService
from book_api.application.use_cases import (
    CreateBookUseCase,
    DeleteBookUseCase,
    GetBookListUseCase,
    GetBookUseCase,
    UpdateBookUseCase,
)
from book_api.gateways.sqlite.database import Database
from book_api.gateways.sqlite.repositories import IBookRepository, SQLiteBookRepository
from book_api.application.services.book import BookService


@lru_cache(1)
def get_container() -> punq.Container:
    return init_container()


def init_container() -> punq.Container:
    container = punq.Container()
    container.register(Database, factory=lambda: Database(), scope=punq.Scope.singleton)
    container.register(IBookRepository, SQLiteBookRepository)
    container.register(IBookService, BookService)
    container.register(GetBookListUseCase)
    container.register(GetBookUseCase)
    container.register(CreateBookUseCase)
    container.register(UpdateBookUseCase)
    container.register(DeleteBookUseCase)
    return container
