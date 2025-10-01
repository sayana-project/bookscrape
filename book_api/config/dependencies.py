"""
Dependency Injection configuration.
This is where we wire up all our dependencies for FastAPI.
"""
from sqlalchemy.orm import Session
from fastapi import Depends

from book_api.infrastructure.database.connection import get_database_session
from book_api.infrastructure.repositories.book_repository import BookRepository
from book_api.infrastructure.repositories.genre_repository import GenreRepository
from book_api.use_cases.services.book_service import BookService
from book_api.use_cases.interfaces.book_repository import IBookRepository
from book_api.use_cases.interfaces.genre_repository import IGenreRepository
from book_api.use_cases.interfaces.book_service import IBookService


def get_book_repository(db: Session = Depends(get_database_session)) -> IBookRepository:
    """
    Dependency to get book repository.
    FastAPI will automatically inject the database session.
    """
    return BookRepository(db)


def get_genre_repository(db: Session = Depends(get_database_session)) -> IGenreRepository:
    """
    Dependency to get genre repository.
    FastAPI will automatically inject the database session.
    """
    return GenreRepository(db)


def get_book_service(
    book_repo: IBookRepository = Depends(get_book_repository),
    genre_repo: IGenreRepository = Depends(get_genre_repository)
) -> IBookService:
    """
    Dependency to get book service.
    FastAPI will automatically inject the repositories.
    """
    return BookService(book_repo, genre_repo)