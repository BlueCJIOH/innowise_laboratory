import pytest

from book_api.application.use_cases import (
    CreateBookUseCase,
    DeleteBookUseCase,
    GetBookListUseCase,
    GetBookUseCase,
    UpdateBookUseCase,
)
from tests.mocks.factories import (
    BookSearchQueryFactory,
    CreateBookCommandFactory,
    DeleteBookCommandFactory,
    GetBookCommandFactory,
    GetBookListCommandFactory,
    PaginationQueryFactory,
    UpdateBookCommandFactory,
)


@pytest.fixture
def mock_get_book_list_use_case(mock_test_container):
    return mock_test_container.resolve(GetBookListUseCase)


@pytest.fixture
def mock_get_book_use_case(mock_test_container):
    return mock_test_container.resolve(GetBookUseCase)


@pytest.fixture
def mock_create_book_use_case(mock_test_container):
    return mock_test_container.resolve(CreateBookUseCase)


@pytest.fixture
def mock_update_book_use_case(mock_test_container):
    return mock_test_container.resolve(UpdateBookUseCase)


@pytest.fixture
def mock_delete_book_use_case(mock_test_container):
    return mock_test_container.resolve(DeleteBookUseCase)


def test_get_book_list(mock_get_book_list_use_case):
    command = GetBookListCommandFactory.build(
        pagination=PaginationQueryFactory.build(),
        search=BookSearchQueryFactory.build(),
    )
    books, _ = mock_get_book_list_use_case.execute(command)

    assert len(books) <= command.pagination.limit


def test_get_book_by_id(mock_get_book_use_case):
    command = GetBookCommandFactory.build()
    book = mock_get_book_use_case.execute(command)

    assert book.id == command.book_id


def test_create_book(mock_create_book_use_case):
    command = CreateBookCommandFactory.build()
    book = mock_create_book_use_case.execute(command)

    assert book.title == command.title
    assert book.author == command.author
    assert book.year == command.year


def test_update_book(mock_update_book_use_case):
    command = UpdateBookCommandFactory.build()
    book = mock_update_book_use_case.execute(command)

    assert book.id == command.book_id


def test_delete_book(mock_delete_book_use_case):
    command = DeleteBookCommandFactory.build()
    result = mock_delete_book_use_case.execute(command)

    assert result is None
