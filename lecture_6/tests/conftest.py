import punq
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from book_api.domain.services import IBookService
from book_api.application.use_cases import (
    CreateBookUseCase,
    DeleteBookUseCase,
    GetBookListUseCase,
    GetBookUseCase,
    UpdateBookUseCase,
)
from book_api.gateways.sqlite.database import Database
from book_api.gateways.sqlite.models import BaseORM
from book_api.gateways.sqlite.repositories import IBookRepository, SQLiteBookRepository
from book_api.application.services.book import BookService
from tests.mocks.services import DummyBookService
from book_api.main import web_app_factory
from book_api.presentation.api.v1.dependencies import get_container


def create_test_database() -> Database:
    db = Database.__new__(Database)
    db.engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    db._session_factory = sessionmaker(bind=db.engine, autocommit=False, autoflush=False)
    db._tables_created = False
    BaseORM.metadata.create_all(bind=db.engine)
    db._tables_created = True
    return db


def create_test_container() -> punq.Container:
    container = punq.Container()

    test_db = create_test_database()
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
    get_container.cache_clear()

    app = web_app_factory()
    app.dependency_overrides[get_container] = lambda: test_container  # type: ignore[index]

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()  # type: ignore[union-attr]
    get_container.cache_clear()
