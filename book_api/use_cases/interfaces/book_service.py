from abc import ABC, abstractmethod
from typing import List, Dict, Any
from book_api.domain.entities.book import Book


class IBookService(ABC):

    @abstractmethod
    def get_all_books(self) -> List[Book]:
        """Get all books."""
        pass

    @abstractmethod
    def search_books(self, keyword: str) -> List[Book]:
        """Search books by keyword."""
        pass

    @abstractmethod
    def get_books_by_genre(self, genre_id: int) -> List[Book]:
        """Get books from specific genre."""
        pass

    @abstractmethod
    def calculate_average_price_all(self) -> Dict[str, Any]:
        """Calculate average price for all books."""
        pass

    @abstractmethod
    def calculate_average_price_by_genre(self, genre_id: int) -> Dict[str, Any]:
        """Calculate average price for books in specific genre."""
        pass

    @abstractmethod
    def calculate_average_stock_all(self) -> Dict[str, Any]:
        """Calculate average stock for all books."""
        pass

    @abstractmethod
    def calculate_average_stock_by_genre(self, genre_id: int) -> Dict[str, Any]:
        """Calculate average stock for books in specific genre."""
        pass