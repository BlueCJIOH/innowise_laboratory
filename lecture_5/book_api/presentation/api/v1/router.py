from fastapi import APIRouter

from book_api.presentation.api.v1.views import books


api_router = APIRouter()
api_router.include_router(books.router, prefix="/books", tags=["books"])