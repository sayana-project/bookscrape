"""
Interface for Genre Repository.
Defines what methods a genre repository must have.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from book_api.domain.entities.genre import Genre


class IGenreRepository(ABC):
    """
    Interface for accessing genre data.
    Any class that implements this must have these methods.
    """

    @abstractmethod
    def get_all(self) -> List[Genre]:
        """Get all genres from database."""
        pass

    @abstractmethod
    def get_by_id(self, genre_id: int) -> Optional[Genre]:
        """Get one genre by its ID."""
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Genre]:
        """Find genre by exact name."""
        pass