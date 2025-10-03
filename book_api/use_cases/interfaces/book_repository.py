from abc import ABC, abstractmethod
from typing import List, Optional
from book_api.domain.entities.book import Book


class IBookRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Book]:
        """Get all books from database."""
        pass

    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Get one book by its ID."""
        pass

    @abstractmethod
    def get_by_keyword(self, keyword: str) -> List[Book]:
        """Find books that contain keyword in title."""
        pass

    @abstractmethod
    def get_by_genre_id(self, genre_id: int) -> List[Book]:
        """Get all books from a specific genre."""
        pass

    @abstractmethod
    def get_books_with_valid_prices(self) -> List[Book]:
        """Get only books that have a valid price."""
        pass