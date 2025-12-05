import punq
import pytest
from fastapi.testclient import TestClient

from book_api.domain.services import IBookService
from book_api.domain.use_cases import (
    CreateBookUseCase,
    DeleteBookUseCase,
    GetBookListUseCase,
    GetBookUseCase,
    UpdateBookUseCase,
)
from book_api.gateways.sqlite.database import Database
from book_api.gateways.sqlite.repositories import IBookRepository, SQLiteBookRepository
from book_api.services.book import BookService
from book_api.tests.mocks.services import DummyBookService
from book_api.main import web_app_factory
from book_api.api.v1.dependencies import get_container


TEST_DATABASE_URL = "sqlite:///:memory:"


def create_test_container() -> punq.Container:
    container = punq.Container()

    test_db = Database(url=TEST_DATABASE_URL)
    test_db.create_tables()
    container.register(Database, instance=test_db)

    container.register(IBookRepository, SQLiteBookRepository)
    container.register(IBookService, BookService)
    container.register(GetBookListUseCase)
    container.register(GetBookUseCase)
    container.register(CreateBookUseCase)
    container.register(UpdateBookUseCase)
    container.register(DeleteBookUseCase)

    return container


@pytest.fixture
def test_container() -> punq.Container:
    return create_test_container()


@pytest.fixture
def mock_test_container() -> punq.Container:
    container = create_test_container()
    container.register(IBookService, DummyBookService)
    return container


@pytest.fixture
def client(test_container):
    app = web_app_factory()
    app.dependency_overrides[get_container] = lambda: test_container  # type: ignore[index]

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()  # type: ignore[union-attr]
