from fastapi import Depends

from book_api.core.container import get_container
from book_api.application.use_cases import (
    CreateBookUseCase,
    DeleteBookUseCase,
    GetBookListUseCase,
    GetBookUseCase,
    UpdateBookUseCase,
)


def get_create_book_use_case(container=Depends(get_container)) -> CreateBookUseCase:
    return container.resolve(CreateBookUseCase)


def get_get_book_use_case(container=Depends(get_container)) -> GetBookUseCase:
    return container.resolve(GetBookUseCase)


def get_update_book_use_case(container=Depends(get_container)) -> UpdateBookUseCase:
    return container.resolve(UpdateBookUseCase)


def get_delete_book_use_case(container=Depends(get_container)) -> DeleteBookUseCase:
    return container.resolve(DeleteBookUseCase)


def get_list_book_use_case(container=Depends(get_container)) -> GetBookListUseCase:
    return container.resolve(GetBookListUseCase)
