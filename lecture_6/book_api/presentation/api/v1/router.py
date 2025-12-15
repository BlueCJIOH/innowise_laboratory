from fastapi import APIRouter

from book_api.presentation.api.v1.views import books
from book_api.presentation.api.v1.views import healthcheck


api_router = APIRouter()
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(healthcheck.router, tags=["healthcheck"])
