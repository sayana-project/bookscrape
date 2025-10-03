from fastapi import APIRouter, Depends, HTTPException
from typing import List

from book_api.config.dependencies import get_book_service
from book_api.config.logging import get_typed_logger
from book_api.use_cases.interfaces.book_service import IBookService
from book_api.interface.dto.book_dto import BookDto, GenreDto
from book_api.interface.dto.response_dto import (
    AveragePriceResponseDto,
    AveragePriceByGenreResponseDto,
    AverageStockResponseDto,
    AverageStockByGenreResponseDto,
    ErrorResponseDto
)

# Create router and logger
router = APIRouter(prefix="/books", tags=["Books"])
logger = get_typed_logger(__name__)


@router.get(
    "",
    response_model=List[BookDto],
    summary="Get all books",
    description="Retrieve all books from the database"
)
def get_all_books(book_service: IBookService = Depends(get_book_service)) -> List[BookDto]:
    try:
        books = book_service.get_all_books()
        return [_convert_book_to_dto(book) for book in books]
    except Exception as e:
        logger.error(f"Error getting all books: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/search/{keyword}",
    response_model=List[BookDto],
    summary="Search books by keyword",
    description="Find books that contain the keyword in their title"
)
def search_books(
    keyword: str,
    book_service: IBookService = Depends(get_book_service)
) -> List[BookDto]:
    try:
        books = book_service.search_books(keyword)
        return [_convert_book_to_dto(book) for book in books]
    except Exception as e:
        logger.error(f"Error searching books with keyword '{keyword}': {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/by_genre/{genre_id}",
    response_model=List[BookDto],
    summary="Get books by genre",
    description="Retrieve all books from a specific genre"
)
def get_books_by_genre(
    genre_id: int,
    book_service: IBookService = Depends(get_book_service)
) -> List[BookDto]:
    try:
        books = book_service.get_books_by_genre(genre_id)
        return [_convert_book_to_dto(book) for book in books]
    except Exception as e:
        logger.error(f"Error getting books for genre {genre_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/average_price/all",
    response_model=AveragePriceResponseDto,
    summary="Calculate average price for all books",
    description="Calculate the average price across all books with valid prices",
    responses={
        200: {"description": "Average price calculated successfully"},
        500: {"model": ErrorResponseDto, "description": "Internal server error"}
    }
)
def get_average_price_all(
    book_service: IBookService = Depends(get_book_service)
) -> AveragePriceResponseDto:
    try:
        logger.info("Calculating average price for all books")
        result = book_service.calculate_average_price_all()

        return AveragePriceResponseDto(
            total_books=result["total_books"],
            books_with_price=result["books_with_price"],
            average_price=result["average_price"]
        )
    except Exception as e:
        logger.error(f"Error calculating average price for all books: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate average price")


@router.get(
    "/average_price/genre/{genre_id}",
    response_model=AveragePriceByGenreResponseDto,
    summary="Calculate average price by genre",
    description="Calculate the average price for books in a specific genre",
    responses={
        200: {"description": "Average price by genre calculated successfully"},
        404: {"model": ErrorResponseDto, "description": "Genre not found"},
        500: {"model": ErrorResponseDto, "description": "Internal server error"}
    }
)
def get_average_price_by_genre(
    genre_id: int,
    book_service: IBookService = Depends(get_book_service)
) -> AveragePriceByGenreResponseDto:
    try:
        logger.info(f"Calculating average price for genre {genre_id}")
        result = book_service.calculate_average_price_by_genre(genre_id)

        return AveragePriceByGenreResponseDto(
            genre_id=result["genre_id"],
            genre_name=result["genre_name"],
            total_books=result["total_books"],
            books_with_price=result["books_with_price"],
            average_price=result["average_price"],
            sample_prices=result["sample_prices"]
        )
    except ValueError as e:
        logger.warning(f"Genre {genre_id} not found: {e}")
        raise HTTPException(status_code=404, detail="Genre not found")
    except Exception as e:
        logger.error(f"Error calculating average price for genre {genre_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate average price")


@router.get(
    "/average_stock/all",
    response_model=AverageStockResponseDto,
    summary="Calculate average stock for all books",
    description="Calculate the average stock across all books"
)
def get_average_stock_all(
    book_service: IBookService = Depends(get_book_service)
) -> AverageStockResponseDto:
    """
    Calculate average stock for all books.
    Clean route that delegates to business service.
    """
    try:
        logger.info("Calculating average stock for all books")
        result = book_service.calculate_average_stock_all()

        return AverageStockResponseDto(
            total_books=result["total_books"],
            books_with_stock=result["books_with_stock"],
            average_stock=result["average_stock"]
        )
    except Exception as e:
        logger.error(f"Error calculating average stock for all books: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate average stock")


@router.get(
    "/average_stock/genre/{genre_id}",
    response_model=AverageStockByGenreResponseDto,
    summary="Calculate average stock by genre",
    description="Calculate the average stock for books in a specific genre"
)
def get_average_stock_by_genre(
    genre_id: int,
    book_service: IBookService = Depends(get_book_service)
) -> AverageStockByGenreResponseDto:
    try:
        logger.info(f"Calculating average stock for genre {genre_id}")
        result = book_service.calculate_average_stock_by_genre(genre_id)

        return AverageStockByGenreResponseDto(
            genre_id=result["genre_id"],
            genre_name=result["genre_name"],
            total_books=result["total_books"],
            books_with_stock=result["books_with_stock"],
            average_stock=result["average_stock"],
            sample_stocks=result["sample_stocks"]
        )
    except ValueError as e:
        logger.warning(f"Genre {genre_id} not found: {e}")
        raise HTTPException(status_code=404, detail="Genre not found")
    except Exception as e:
        logger.error(f"Error calculating average stock for genre {genre_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate average stock")


def _convert_book_to_dto(book) -> BookDto:
    return BookDto(
        id=book.id,
        title=book.title,
        genre_id=book.genre_id,
        note=book.note,
        stock_number=book.stock_number,
        datetime=book.datetime,
        upc=book.upc,
        product_type=book.product_type,
        price_ht=float(book.price_ht) if book.price_ht else None,
        price_taxed=float(book.price_taxed) if book.price_taxed else None,
        review_number=book.review_number,
        description=book.description
    )