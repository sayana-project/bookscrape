"""
Response DTOs for API responses.
These define the structure of API response data.
"""
from pydantic import BaseModel, Field
from typing import List, Any


class AveragePriceResponseDto(BaseModel):
    """
    DTO for average price calculation responses.
    """
    total_books: int = Field(..., description="Total number of books")
    books_with_price: int = Field(..., description="Number of books with valid prices")
    average_price: float = Field(..., description="Average price")

    class Config:
        json_schema_extra = {
            "example": {
                "total_books": 100,
                "books_with_price": 85,
                "average_price": 12.50
            }
        }


class AveragePriceByGenreResponseDto(BaseModel):
    """
    DTO for average price by genre responses.
    """
    genre_id: int = Field(..., description="Genre ID")
    genre_name: str = Field(..., description="Genre name")
    total_books: int = Field(..., description="Total books in genre")
    books_with_price: int = Field(..., description="Books with valid prices")
    average_price: float = Field(..., description="Average price")
    sample_prices: List[float] = Field(..., description="Sample of first 10 prices")

    class Config:
        json_schema_extra = {
            "example": {
                "genre_id": 1,
                "genre_name": "Fiction",
                "total_books": 20,
                "books_with_price": 18,
                "average_price": 15.75,
                "sample_prices": [12.99, 18.50, 14.25]
            }
        }


class AverageStockResponseDto(BaseModel):
    """
    DTO for average stock calculation responses.
    """
    total_books: int = Field(..., description="Total number of books")
    books_with_stock: int = Field(..., description="Number of books with stock info")
    average_stock: int = Field(..., description="Average stock number")

    class Config:
        json_schema_extra = {
            "example": {
                "total_books": 100,
                "books_with_stock": 95,
                "average_stock": 15
            }
        }


class AverageStockByGenreResponseDto(BaseModel):
    """
    DTO for average stock by genre responses.
    """
    genre_id: int = Field(..., description="Genre ID")
    genre_name: str = Field(..., description="Genre name")
    total_books: int = Field(..., description="Total books in genre")
    books_with_stock: int = Field(..., description="Books with stock info")
    average_stock: int = Field(..., description="Average stock number")
    sample_stocks: List[int] = Field(..., description="Sample of first 10 stock numbers")

    class Config:
        json_schema_extra = {
            "example": {
                "genre_id": 1,
                "genre_name": "Fiction",
                "total_books": 20,
                "books_with_stock": 19,
                "average_stock": 12,
                "sample_stocks": [10, 15, 8, 20, 5]
            }
        }


class ErrorResponseDto(BaseModel):
    """
    Standard error response DTO.
    """
    detail: str = Field(..., description="Error description")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Genre not found"
            }
        }