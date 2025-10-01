"""
Genre API Router - Clean Architecture version.
Simple router for genre operations.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from book_api.config.dependencies import get_genre_repository
from book_api.config.logging import get_typed_logger
from book_api.use_cases.interfaces.genre_repository import IGenreRepository
from book_api.interface.dto.book_dto import GenreDto
from book_api.interface.dto.response_dto import ErrorResponseDto

# Create router and logger
router = APIRouter(prefix="/genres", tags=["Genres"])
logger = get_typed_logger(__name__)


@router.get(
    "",
    response_model=List[GenreDto],
    summary="Get all genres",
    description="Retrieve all available genres",
    responses={
        200: {"description": "List of genres retrieved successfully"},
        500: {"model": ErrorResponseDto, "description": "Internal server error"}
    }
)
def get_all_genres(
    genre_repo: IGenreRepository = Depends(get_genre_repository)
) -> List[GenreDto]:
    """
    Get all genres.
    Simple clean route.
    """
    try:
        logger.info("Getting all genres")
        genres = genre_repo.get_all()
        return [_convert_genre_to_dto(genre) for genre in genres]
    except Exception as e:
        logger.error(f"Error getting all genres: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{genre_id}",
    response_model=GenreDto,
    summary="Get genre by ID",
    description="Retrieve a specific genre by its ID",
    responses={
        200: {"description": "Genre retrieved successfully"},
        404: {"model": ErrorResponseDto, "description": "Genre not found"},
        500: {"model": ErrorResponseDto, "description": "Internal server error"}
    }
)
def get_genre_by_id(
    genre_id: int,
    genre_repo: IGenreRepository = Depends(get_genre_repository)
) -> GenreDto:
    """
    Get genre by ID.
    Clean route with proper error handling.
    """
    try:
        logger.info(f"Getting genre with ID: {genre_id}")
        genre = genre_repo.get_by_id(genre_id)
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
        return _convert_genre_to_dto(genre)
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error getting genre {genre_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def _convert_genre_to_dto(genre) -> GenreDto:
    """
    Convert domain entity to DTO.
    Helper function to keep routes clean.
    """
    return GenreDto(
        id=genre.id,
        name=genre.name
    )