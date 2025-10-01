"""
Book Service - Contains all business logic for books.
This is where we put calculations, validations, and business rules.
"""
from typing import List, Dict, Any
import logging

from book_api.use_cases.interfaces.book_service import IBookService
from book_api.use_cases.interfaces.book_repository import IBookRepository
from book_api.use_cases.interfaces.genre_repository import IGenreRepository
from book_api.domain.entities.book import Book

logger = logging.getLogger(__name__)


class BookService(IBookService):
    """
    Service that contains business logic for books.
    This is where we put all the calculations and business rules.
    """

    def __init__(self, book_repo: IBookRepository, genre_repo: IGenreRepository):
        self.book_repo = book_repo
        self.genre_repo = genre_repo

    def get_all_books(self) -> List[Book]:
        """Get all books."""
        logger.info("Getting all books")
        return self.book_repo.get_all()

    def search_books(self, keyword: str) -> List[Book]:
        """Search books by keyword."""
        logger.info(f"Searching books with keyword: {keyword}")
        return self.book_repo.get_by_keyword(keyword)

    def get_books_by_genre(self, genre_id: int) -> List[Book]:
        """Get books from specific genre."""
        logger.info(f"Getting books for genre ID: {genre_id}")
        return self.book_repo.get_by_genre_id(genre_id)

    def calculate_average_price_all(self) -> Dict[str, Any]:
        """
        Calculate average price for all books.
        Business logic: only count books with valid prices.
        """
        logger.info("Calculating average price for all books")

        all_books = self.book_repo.get_all()
        books_with_price = [book for book in all_books if book.has_valid_price()]

        if not books_with_price:
            return {
                "total_books": len(all_books),
                "books_with_price": 0,
                "average_price": 0.0,
            }

        # Business logic: calculate average
        total_price = sum(float(book.price_taxed) for book in books_with_price)
        average = round(total_price / len(books_with_price), 2)

        logger.info(f"Average calculated on {len(books_with_price)} valid books out of {len(all_books)}")

        return {
            "total_books": len(all_books),
            "books_with_price": len(books_with_price),
            "average_price": average,
        }

    def calculate_average_price_by_genre(self, genre_id: int) -> Dict[str, Any]:
        """
        Calculate average price for books in specific genre.
        """
        logger.info(f"Calculating average price for genre ID: {genre_id}")

        # Get genre info
        genre = self.genre_repo.get_by_id(genre_id)
        if not genre:
            raise ValueError("Genre not found")

        # Get books for this genre
        books = self.book_repo.get_by_genre_id(genre_id)
        books_with_price = [book for book in books if book.has_valid_price()]

        if not books_with_price:
            average = 0.0
            sample_prices = []
        else:
            total_price = sum(float(book.price_taxed) for book in books_with_price)
            average = round(total_price / len(books_with_price), 2)
            sample_prices = [float(book.price_taxed) for book in books_with_price[:10]]

        logger.info(f"Genre {genre.name} ({genre_id}) → {len(books_with_price)} valid prices out of {len(books)} books")

        return {
            "genre_id": genre_id,
            "genre_name": genre.name,
            "total_books": len(books),
            "books_with_price": len(books_with_price),
            "average_price": average,
            "sample_prices": sample_prices
        }

    def calculate_average_stock_all(self) -> Dict[str, Any]:
        """
        Calculate average stock for all books.
        """
        logger.info("Calculating average stock for all books")

        all_books = self.book_repo.get_all()
        books_with_stock = [book for book in all_books if book.stock_number is not None]

        if not books_with_stock:
            return {
                "total_books": len(all_books),
                "books_with_stock": 0,
                "average_stock": 0,
            }

        total_stock = sum(book.stock_number for book in books_with_stock)
        average = round(total_stock / len(books_with_stock), 0)

        logger.info(f"Average calculated on {len(books_with_stock)} valid stocks out of {len(all_books)}")

        return {
            "total_books": len(all_books),
            "books_with_stock": len(books_with_stock),
            "average_stock": int(average),
        }

    def calculate_average_stock_by_genre(self, genre_id: int) -> Dict[str, Any]:
        """
        Calculate average stock for books in specific genre.
        """
        logger.info(f"Calculating average stock for genre ID: {genre_id}")

        # Get genre info
        genre = self.genre_repo.get_by_id(genre_id)
        if not genre:
            raise ValueError("Genre not found")

        # Get books for this genre
        books = self.book_repo.get_by_genre_id(genre_id)
        books_with_stock = [book for book in books if book.stock_number is not None]

        if not books_with_stock:
            average = 0
            sample_stocks = []
        else:
            total_stock = sum(book.stock_number for book in books_with_stock)
            average = round(total_stock / len(books_with_stock), 0)
            sample_stocks = [book.stock_number for book in books_with_stock[:10]]

        logger.info(f"Genre {genre.name} ({genre_id}) → {len(books_with_stock)} valid stocks out of {len(books)} books")

        return {
            "genre_id": genre_id,
            "genre_name": genre.name,
            "total_books": len(books),
            "books_with_stock": len(books_with_stock),
            "average_stock": int(average),
            "sample_stocks": sample_stocks
        }