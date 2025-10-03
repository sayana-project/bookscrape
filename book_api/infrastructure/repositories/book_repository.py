"""
Concrete implementation of Book Repository.
This class actually talks to the database.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from decimal import Decimal

from book_api.use_cases.interfaces.book_repository import IBookRepository
from book_api.domain.entities.book import Book
from book_api.infrastructure.database.models import BookModel


class BookRepository(IBookRepository):
    """
    Concrete implementation of book repository.
    Handles database operations for books.
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all(self) -> List[Book]:
        """Get all books from database."""
        db_books = self.db.query(BookModel).all()
        return [self._convert_to_entity(db_book) for db_book in db_books]

    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Get one book by its ID."""
        db_book = self.db.query(BookModel).filter(BookModel.id == book_id).first()
        if db_book:
            return self._convert_to_entity(db_book)
        return None

    def get_by_keyword(self, keyword: str) -> List[Book]:
        """Find books that contain keyword in title."""
        db_books = self.db.query(BookModel).filter(
            BookModel.title.ilike(f"%{keyword}%")
        ).all()
        return [self._convert_to_entity(db_book) for db_book in db_books]

    def get_by_genre_id(self, genre_id: int) -> List[Book]:
        """Get all books from a specific genre."""
        db_books = self.db.query(BookModel).filter(
            BookModel.genre_id == genre_id
        ).all()
        return [self._convert_to_entity(db_book) for db_book in db_books]

    def get_books_with_valid_prices(self) -> List[Book]:
        """Get only books that have a valid price."""
        db_books = self.db.query(BookModel).filter(
            BookModel.price_taxed.isnot(None)
        ).all()
        return [self._convert_to_entity(db_book) for db_book in db_books]

    def _convert_to_entity(self, db_book: BookModel) -> Book:
        """
        Convert database model to domain entity.
        This separates database concerns from business logic.
        """
        return Book(
            id=db_book.id,
            title=db_book.title,
            genre_id=db_book.genre_id,
            note=db_book.note,
            stock_number=db_book.stock_number,
            datetime=db_book.datetime,
            upc=db_book.upc,
            product_type=db_book.product_type,
            price_ht=Decimal(str(db_book.price_ht)) if db_book.price_ht else None,
            price_taxed=Decimal(str(db_book.price_taxed)) if db_book.price_taxed else None,
            review_number=db_book.review_number,
            description=db_book.description
        )