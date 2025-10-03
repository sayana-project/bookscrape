from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class Book:
    id: int
    title: str
    genre_id: int
    note: Optional[int] = None
    stock_number: Optional[int] = None
    datetime: Optional[str] = None
    upc: Optional[str] = None
    product_type: Optional[str] = None
    price_ht: Optional[Decimal] = None
    price_taxed: Optional[Decimal] = None
    review_number: Optional[int] = None
    description: Optional[str] = None

    def __post_init__(self):
        """Validate business rules after initialization."""
        self._validate_note()
        self._validate_stock()
        self._validate_prices()

    def _validate_note(self) -> None:
        """Validate that note is between 1 and 5."""
        if self.note is not None and not (1 <= self.note <= 5):
            raise ValueError("Note must be between 1 and 5")

    def _validate_stock(self) -> None:
        """Validate that stock number is non-negative."""
        if self.stock_number is not None and self.stock_number < 0:
            raise ValueError("Stock number cannot be negative")

    def _validate_prices(self) -> None:
        """Validate that prices are positive."""
        if self.price_ht is not None and self.price_ht < 0:
            raise ValueError("Price HT cannot be negative")
        if self.price_taxed is not None and self.price_taxed < 0:
            raise ValueError("Price taxed cannot be negative")

    def is_in_stock(self) -> bool:
        """Check if book is in stock."""
        return self.stock_number is not None and self.stock_number > 0

    def has_valid_price(self) -> bool:
        """Check if book has a valid taxed price."""
        return self.price_taxed is not None and self.price_taxed > 0

    def calculate_tax_amount(self) -> Optional[Decimal]:
        """Calculate tax amount if both prices are available."""
        if self.price_ht is not None and self.price_taxed is not None:
            return self.price_taxed - self.price_ht
        return None

    def get_formatted_title(self) -> str:
        """Get formatted title for display."""
        return self.title.strip().title() if self.title else "Untitled"