"""
Concrete implementation of Genre Repository.
This class actually talks to the database.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from book_api.use_cases.interfaces.genre_repository import IGenreRepository
from book_api.domain.entities.genre import Genre
from book_api.infrastructure.database.models import GenreModel


class GenreRepository(IGenreRepository):
    """
    Concrete implementation of genre repository.
    Handles database operations for genres.
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all(self) -> List[Genre]:
        """Get all genres from database."""
        db_genres = self.db.query(GenreModel).all()
        return [self._convert_to_entity(db_genre) for db_genre in db_genres]

    def get_by_id(self, genre_id: int) -> Optional[Genre]:
        """Get one genre by its ID."""
        db_genre = self.db.query(GenreModel).filter(GenreModel.id == genre_id).first()
        if db_genre:
            return self._convert_to_entity(db_genre)
        return None

    def get_by_name(self, name: str) -> Optional[Genre]:
        """Find genre by exact name."""
        db_genre = self.db.query(GenreModel).filter(GenreModel.genre == name).first()
        if db_genre:
            return self._convert_to_entity(db_genre)
        return None

    def _convert_to_entity(self, db_genre: GenreModel) -> Genre:
        """
        Convert database model to domain entity.
        This separates database concerns from business logic.
        """
        return Genre(
            id=db_genre.id,
            name=db_genre.genre
        )