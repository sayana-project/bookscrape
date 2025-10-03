"""
Value object for handling prices.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class Price:
    """
    Price value object for handling monetary values.
    Immutable and contains price validation logic.
    """
    amount: Decimal

    def __post_init__(self):
        """Validate price amount."""
        if self.amount < 0:
            raise ValueError("Price cannot be negative")

    @classmethod
    def from_float(cls, value: float) -> 'Price':
        """Create Price from float value."""
        return cls(Decimal(str(value)))

    def to_float(self) -> float:
        """Convert price to float."""
        return float(self.amount)

    def add_tax(self, tax_rate: Decimal) -> 'Price':
        """Add tax to price and return new Price object."""
        tax_amount = self.amount * tax_rate
        return Price(self.amount + tax_amount)

    def format_euro(self) -> str:
        """Format price in euros."""
        return f"€{self.amount:.2f}"