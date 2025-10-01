"""
Domain entity for Genre.
Simple entity representing a book genre.
"""
from dataclasses import dataclass


@dataclass
class Genre:
    """
    Genre domain entity.
    Represents a book genre category.
    """
    id: int
    name: str

    def __post_init__(self):
        """Validate genre name."""
        if not self.name or not self.name.strip():
            raise ValueError("Genre name cannot be empty")

        # Clean the name
        self.name = self.name.strip().title()

    def is_valid(self) -> bool:
        """Check if genre is valid."""
        return len(self.name) > 0