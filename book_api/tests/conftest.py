"""
Pytest configuration and fixtures.
"""
import pytest
from decimal import Decimal

from book_api.domain.entities.book import Book
from book_api.domain.entities.genre import Genre


@pytest.fixture
def sample_book():
    """Fixture that provides a sample book for testing."""
    return Book(
        id=1,
        title="Sample Book",
        genre_id=1,
        note=4,
        stock_number=10,
        price_ht=Decimal("10.00"),
        price_taxed=Decimal("12.00"),
        description="A sample book for testing"
    )


@pytest.fixture
def sample_genre():
    """Fixture that provides a sample genre for testing."""
    return Genre(id=1, name="Fiction")


@pytest.fixture
def sample_books_list():
    """Fixture that provides a list of sample books."""
    return [
        Book(id=1, title="Book 1", genre_id=1, price_taxed=Decimal("10.00")),
        Book(id=2, title="Book 2", genre_id=1, price_taxed=Decimal("20.00")),
        Book(id=3, title="Book 3", genre_id=2, price_taxed=None),
    ]