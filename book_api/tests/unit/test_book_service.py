"""
Unit tests for BookService.
These tests use mocks to isolate the business logic.
"""
import pytest
from unittest.mock import Mock
from decimal import Decimal

from book_api.use_cases.services.book_service import BookService
from book_api.domain.entities.book import Book
from book_api.domain.entities.genre import Genre


class TestBookService:
    """Test class for BookService business logic."""

    def setup_method(self):
        """Setup test dependencies before each test."""
        # Create mock repositories
        self.mock_book_repo = Mock()
        self.mock_genre_repo = Mock()

        # Create service with mocked dependencies
        self.service = BookService(self.mock_book_repo, self.mock_genre_repo)

    def test_calculate_average_price_all_with_valid_books(self):
        """Test average price calculation with valid books."""
        # Arrange: Create test data
        test_books = [
            Book(id=1, title="Book 1", genre_id=1, price_taxed=Decimal("10.00")),
            Book(id=2, title="Book 2", genre_id=1, price_taxed=Decimal("20.00")),
            Book(id=3, title="Book 3", genre_id=1, price_taxed=None),  # No price
        ]

        # Mock repository behavior
        self.mock_book_repo.get_all.return_value = test_books

        # Act: Call the method
        result = self.service.calculate_average_price_all()

        # Assert: Check results
        assert result["total_books"] == 3
        assert result["books_with_price"] == 2
        assert result["average_price"] == 15.00

        # Verify repository was called
        self.mock_book_repo.get_all.assert_called_once()

    def test_calculate_average_price_all_with_no_valid_prices(self):
        """Test average price calculation when no books have valid prices."""
        # Arrange: Create books without prices
        test_books = [
            Book(id=1, title="Book 1", genre_id=1, price_taxed=None),
            Book(id=2, title="Book 2", genre_id=1, price_taxed=None),
        ]

        self.mock_book_repo.get_all.return_value = test_books

        # Act
        result = self.service.calculate_average_price_all()

        # Assert
        assert result["total_books"] == 2
        assert result["books_with_price"] == 0
        assert result["average_price"] == 0.0

    def test_calculate_average_price_by_genre_success(self):
        """Test average price calculation by genre."""
        # Arrange: Create test data
        test_genre = Genre(id=1, name="Fiction")
        test_books = [
            Book(id=1, title="Book 1", genre_id=1, price_taxed=Decimal("15.00")),
            Book(id=2, title="Book 2", genre_id=1, price_taxed=Decimal("25.00")),
        ]

        # Mock repository behavior
        self.mock_genre_repo.get_by_id.return_value = test_genre
        self.mock_book_repo.get_by_genre_id.return_value = test_books

        # Act
        result = self.service.calculate_average_price_by_genre(1)

        # Assert
        assert result["genre_id"] == 1
        assert result["genre_name"] == "Fiction"
        assert result["total_books"] == 2
        assert result["books_with_price"] == 2
        assert result["average_price"] == 20.00
        assert len(result["sample_prices"]) == 2

        # Verify both repositories were called
        self.mock_genre_repo.get_by_id.assert_called_once_with(1)
        self.mock_book_repo.get_by_genre_id.assert_called_once_with(1)

    def test_calculate_average_price_by_genre_not_found(self):
        """Test error handling when genre doesn't exist."""
        # Arrange: Mock repository to return None
        self.mock_genre_repo.get_by_id.return_value = None

        # Act & Assert: Expect ValueError
        with pytest.raises(ValueError, match="Genre not found"):
            self.service.calculate_average_price_by_genre(999)

    def test_search_books(self):
        """Test book search functionality."""
        # Arrange
        keyword = "python"
        expected_books = [
            Book(id=1, title="Python Programming", genre_id=1),
            Book(id=2, title="Learn Python", genre_id=1),
        ]

        self.mock_book_repo.get_by_keyword.return_value = expected_books

        # Act
        result = self.service.search_books(keyword)

        # Assert
        assert len(result) == 2
        assert result[0].title == "Python Programming"
        self.mock_book_repo.get_by_keyword.assert_called_once_with(keyword)

    def test_calculate_average_stock_all(self):
        """Test average stock calculation."""
        # Arrange
        test_books = [
            Book(id=1, title="Book 1", genre_id=1, stock_number=10),
            Book(id=2, title="Book 2", genre_id=1, stock_number=20),
            Book(id=3, title="Book 3", genre_id=1, stock_number=None),  # No stock
        ]

        self.mock_book_repo.get_all.return_value = test_books

        # Act
        result = self.service.calculate_average_stock_all()

        # Assert
        assert result["total_books"] == 3
        assert result["books_with_stock"] == 2
        assert result["average_stock"] == 15  # (10 + 20) / 2