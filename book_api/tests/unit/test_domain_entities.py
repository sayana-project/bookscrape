"""
Unit tests for domain entities.
Tests business rules and validation logic.
"""
import pytest
from decimal import Decimal

from book_api.domain.entities.book import Book
from book_api.domain.entities.genre import Genre


class TestBookEntity:
    """Test class for Book domain entity."""

    def test_book_creation_valid(self):
        """Test creating a valid book."""
        book = Book(
            id=1,
            title="Test Book",
            genre_id=1,
            note=4,
            stock_number=10,
            price_ht=Decimal("10.00"),
            price_taxed=Decimal("12.00")
        )

        assert book.id == 1
        assert book.title == "Test Book"
        assert book.note == 4

    def test_book_invalid_note_too_high(self):
        """Test that note validation works for values too high."""
        with pytest.raises(ValueError, match="Note must be between 1 and 5"):
            Book(id=1, title="Test", genre_id=1, note=6)

    def test_book_invalid_note_too_low(self):
        """Test that note validation works for values too low."""
        with pytest.raises(ValueError, match="Note must be between 1 and 5"):
            Book(id=1, title="Test", genre_id=1, note=0)

    def test_book_negative_stock(self):
        """Test that negative stock is not allowed."""
        with pytest.raises(ValueError, match="Stock number cannot be negative"):
            Book(id=1, title="Test", genre_id=1, stock_number=-1)

    def test_book_negative_price(self):
        """Test that negative prices are not allowed."""
        with pytest.raises(ValueError, match="Price taxed cannot be negative"):
            Book(id=1, title="Test", genre_id=1, price_taxed=Decimal("-1.00"))

    def test_is_in_stock_true(self):
        """Test is_in_stock method when book is in stock."""
        book = Book(id=1, title="Test", genre_id=1, stock_number=5)
        assert book.is_in_stock() is True

    def test_is_in_stock_false(self):
        """Test is_in_stock method when book is not in stock."""
        book = Book(id=1, title="Test", genre_id=1, stock_number=0)
        assert book.is_in_stock() is False

    def test_is_in_stock_none(self):
        """Test is_in_stock method when stock is None."""
        book = Book(id=1, title="Test", genre_id=1, stock_number=None)
        assert book.is_in_stock() is False

    def test_has_valid_price_true(self):
        """Test has_valid_price method with valid price."""
        book = Book(id=1, title="Test", genre_id=1, price_taxed=Decimal("10.00"))
        assert book.has_valid_price() is True

    def test_has_valid_price_false(self):
        """Test has_valid_price method with no price."""
        book = Book(id=1, title="Test", genre_id=1, price_taxed=None)
        assert book.has_valid_price() is False

    def test_calculate_tax_amount(self):
        """Test tax amount calculation."""
        book = Book(
            id=1, title="Test", genre_id=1,
            price_ht=Decimal("10.00"),
            price_taxed=Decimal("12.00")
        )
        tax_amount = book.calculate_tax_amount()
        assert tax_amount == Decimal("2.00")

    def test_get_formatted_title(self):
        """Test title formatting."""
        book = Book(id=1, title="  test book  ", genre_id=1)
        assert book.get_formatted_title() == "Test Book"


class TestGenreEntity:
    """Test class for Genre domain entity."""

    def test_genre_creation_valid(self):
        """Test creating a valid genre."""
        genre = Genre(id=1, name="Fiction")
        assert genre.id == 1
        assert genre.name == "Fiction"

    def test_genre_empty_name(self):
        """Test that empty genre name is not allowed."""
        with pytest.raises(ValueError, match="Genre name cannot be empty"):
            Genre(id=1, name="")

    def test_genre_whitespace_name(self):
        """Test that whitespace-only genre name is not allowed."""
        with pytest.raises(ValueError, match="Genre name cannot be empty"):
            Genre(id=1, name="   ")

    def test_genre_name_formatting(self):
        """Test that genre name gets formatted properly."""
        genre = Genre(id=1, name="  fiction  ")
        assert genre.name == "Fiction"

    def test_is_valid_true(self):
        """Test is_valid method with valid genre."""
        genre = Genre(id=1, name="Fiction")
        assert genre.is_valid() is True