from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class BookModel(Base):
    __tablename__ = "python_books"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    author: Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )
    publisher: Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )
    year: Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(4),
        nullable=True
    )