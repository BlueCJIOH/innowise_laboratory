from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from book_api.domain.entities import Book
from book_api.gateways.sqlite.database import Database
from book_api.gateways.sqlite.models import BookORM


@dataclass
class IBookRepository(ABC):
    database: Database

    @property
    def session(self) -> Session:
        return self.database.connection

    @abstractmethod
    def get_by_id(self, oid: int) -> Book | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, *, title: str, author: str, year: int | None) -> Book:
        raise NotImplementedError

    @abstractmethod
    def update(self, oid: int, *, title: str | None, author: str | None, year: int | None) -> Book | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, oid: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def find_many(self, *, title: str | None, author: str | None, year: int | None, offset: int, limit: int) -> list[Book]:
        raise NotImplementedError

    @abstractmethod
    def count_many(self, *, title: str | None, author: str | None, year: int | None) -> int:
        raise NotImplementedError


@dataclass
class SQLiteBookRepository(IBookRepository):
    def _filtered_query(self, title: str | None, author: str | None, year: int | None):
        query = select(BookORM)
        if title:
            query = query.where(BookORM.title.ilike(f"%{title}%"))
        if author:
            query = query.where(BookORM.author.ilike(f"%{author}%"))
        if year is not None:
            query = query.where(BookORM.year == year)
        return query

    def get_by_id(self, oid: int) -> Book | None:
        with self.session as session:
            book = session.get(BookORM, oid)
            return book.to_entity() if book else None

    def create(self, *, title: str, author: str, year: int | None) -> Book:
        with self.session as session:
            book = BookORM(title=title, author=author, year=year)
            session.add(book)
            session.commit()
            session.refresh(book)
            return book.to_entity()

    def update(self, oid: int, *, title: str | None, author: str | None, year: int | None) -> Book | None:
        with self.session as session:
            book = session.get(BookORM, oid)
            if not book:
                return None
            if title is not None:
                book.title = title
            if author is not None:
                book.author = author
            if year is not None:
                book.year = year
            session.commit()
            session.refresh(book)
            return book.to_entity()

    def delete(self, oid: int) -> bool:
        with self.session as session:
            book = session.get(BookORM, oid)
            if not book:
                return False
            session.delete(book)
            session.commit()
            return True

    def find_many(self, *, title: str | None, author: str | None, year: int | None, offset: int, limit: int) -> list[Book]:
        with self.session as session:
            query = self._filtered_query(title, author, year).order_by(BookORM.id).offset(offset).limit(limit)
            books = session.scalars(query).all()
            return [b.to_entity() for b in books if b]

    def count_many(self, *, title: str | None, author: str | None, year: int | None) -> int:
        with self.session as session:
            query = self._filtered_query(title, author, year)
            count_query = select(func.count()).select_from(query.subquery())
            return session.execute(count_query).scalar_one()
