import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from book_api.domain.entities import Book as BookEntity
from book_api.gateways.sqlite.models.base import BaseORM


class BookORM(BaseORM):
    __tablename__ = "books"

    id: Mapped[int | None] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, index=True, nullable=False)
    author: Mapped[str] = mapped_column(sa.String, index=True, nullable=False)
    year: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)

    @staticmethod
    def from_entity(entity: BookEntity) -> "BookORM":
        return BookORM(
            id=entity.id,
            title=entity.title,
            author=entity.author,
            year=entity.year,
        )

    def to_entity(self) -> BookEntity:
        return BookEntity(
            id=self.id if self.id is not None else 0,
            title=self.title,
            author=self.author,
            year=self.year,
        )
