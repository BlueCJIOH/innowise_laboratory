from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from book_api.core.configs import settings
from book_api.gateways.sqlite.models import BaseORM


class Database:
    def __init__(self, url: str | None = None) -> None:
        db_url = url or settings.sqlite_url
        connect_args = {"check_same_thread": False}
        self.engine = create_engine(db_url, connect_args=connect_args)
        self._session_factory = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        self._tables_created = False

    @property
    def connection(self) -> Session:
        return self._session_factory()

    def create_tables(self) -> None:
        if self._tables_created:
            return
        BaseORM.metadata.create_all(bind=self.engine)
        self._tables_created = True

    def close(self) -> None:
        self.engine.dispose()
