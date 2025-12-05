from fastapi import APIRouter, Depends, HTTPException, Query, status

from book_api.api.v1.schemas import (
    ApiResponse,
    BookInSchema,
    BookOutSchema,
    BookUpdateSchema,
    ListPaginatedResponse,
    PaginationOutSchema,
)
from book_api.api.v1.dependencies import (
    get_create_book_use_case,
    get_delete_book_use_case,
    get_get_book_use_case,
    get_list_book_use_case,
    get_update_book_use_case,
)
from book_api.domain.commands import (
    BookSearchQuery,
    CreateBookCommand,
    DeleteBookCommand,
    GetBookCommand,
    GetBookListCommand,
    PaginationQuery,
    UpdateBookCommand,
)
from book_api.domain.errors import BookNotFound
from book_api.domain.use_cases import (
    CreateBookUseCase,
    DeleteBookUseCase,
    GetBookListUseCase,
    GetBookUseCase,
    UpdateBookUseCase,
)

router = APIRouter()


def get_pagination(page: int = 0, limit: int = 10) -> PaginationQuery:
    return PaginationQuery(page=page, limit=limit)


def get_all_books_command(
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetBookListCommand:
    return GetBookListCommand(pagination=pagination)


def get_search_command(
    title: str | None = Query(default=None),
    author: str | None = Query(default=None),
    year: int | None = Query(default=None),
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetBookListCommand:
    return GetBookListCommand(
        search=BookSearchQuery(title=title, author=author, year=year),
        pagination=pagination,
    )


@router.get("/", response_model=ApiResponse[ListPaginatedResponse[BookOutSchema]])
def get_all_books_view(
    command: GetBookListCommand = Depends(get_all_books_command),
    use_case: GetBookListUseCase = Depends(get_list_book_use_case),
) -> ApiResponse[ListPaginatedResponse[BookOutSchema]]:
    """Получить все книги (с пагинацией)."""
    books, count = use_case.execute(command)
    response = ListPaginatedResponse(
        items=[BookOutSchema.from_entity(book) for book in books],
        pagination=PaginationOutSchema(
            page=command.pagination.page,
            limit=command.pagination.limit,
            total=count,
        ),
    )
    return ApiResponse(data=response)


@router.post("/", response_model=ApiResponse[BookOutSchema], status_code=status.HTTP_201_CREATED)
def create_book_view(
    payload: BookInSchema,
    use_case: CreateBookUseCase = Depends(get_create_book_use_case),
) -> ApiResponse[BookOutSchema]:
    command = CreateBookCommand(title=payload.title, author=payload.author, year=payload.year)
    book = use_case.execute(command)
    return ApiResponse(data=BookOutSchema.from_entity(book))


@router.get("/search/", response_model=ApiResponse[ListPaginatedResponse[BookOutSchema]])
def search_books_view(
    command: GetBookListCommand = Depends(get_search_command),
    use_case: GetBookListUseCase = Depends(get_list_book_use_case),
) -> ApiResponse[ListPaginatedResponse[BookOutSchema]]:
    """Поиск книг по title, author, year."""
    books, count = use_case.execute(command)
    response = ListPaginatedResponse(
        items=[BookOutSchema.from_entity(book) for book in books],
        pagination=PaginationOutSchema(
            page=command.pagination.page,
            limit=command.pagination.limit,
            total=count,
        ),
    )
    return ApiResponse(data=response)


@router.get("/{book_id}", response_model=ApiResponse[BookOutSchema])
def get_book_view(
    book_id: int,
    use_case: GetBookUseCase = Depends(get_get_book_use_case),
) -> ApiResponse[BookOutSchema]:
    command = GetBookCommand(book_id=book_id)
    try:
        book = use_case.execute(command)
    except BookNotFound as error:
        raise HTTPException(status_code=404, detail="Book not found") from error
    return ApiResponse(data=BookOutSchema.from_entity(book))


@router.put("/{book_id}", response_model=ApiResponse[BookOutSchema])
def update_book_view(
    book_id: int,
    payload: BookUpdateSchema,
    use_case: UpdateBookUseCase = Depends(get_update_book_use_case),
) -> ApiResponse[BookOutSchema]:
    command = UpdateBookCommand(book_id=book_id, title=payload.title, author=payload.author, year=payload.year)
    try:
        book = use_case.execute(command)
    except BookNotFound as error:
        raise HTTPException(status_code=404, detail="Book not found") from error
    return ApiResponse(data=BookOutSchema.from_entity(book))


@router.delete("/{book_id}", response_model=ApiResponse[dict])
def delete_book_view(
    book_id: int,
    use_case: DeleteBookUseCase = Depends(get_delete_book_use_case),
) -> ApiResponse[dict]:
    command = DeleteBookCommand(book_id=book_id)
    try:
        use_case.execute(command)
    except BookNotFound as error:
        raise HTTPException(status_code=404, detail="Book not found") from error
    return ApiResponse(data={})
