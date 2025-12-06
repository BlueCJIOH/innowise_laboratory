from contextlib import asynccontextmanager

from fastapi import FastAPI

from book_api.presentation.api.v1.router import api_router
from book_api.core.container import get_container
from book_api.gateways.sqlite.database import Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = get_container()
    db = container.resolve(Database)
    db.create_tables()
    yield
    db.close()


def web_app_factory() -> FastAPI:
    app = FastAPI(title="Book API Gateway", lifespan=lifespan)
    app.include_router(api_router)
    return app


app = web_app_factory()