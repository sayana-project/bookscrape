"""
Data Transfer Objects (DTOs) for Book API.
These define how data is sent in/out of the API.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal


class BookDto(BaseModel):
    """
    DTO for book data.
    This is what gets returned by the API.
    """
    id: int
    title: Optional[str] = Field(None, description="Book title")
    genre_id: Optional[int] = Field(None, description="ID of the genre")
    note: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1 to 5")
    stock_number: Optional[int] = Field(None, ge=0, description="Number in stock")
    datetime: Optional[str] = Field(None, description="Date and time")
    upc: Optional[str] = Field(None, description="Universal Product Code")
    product_type: Optional[str] = Field(None, description="Type of product")
    price_ht: Optional[float] = Field(None, ge=0, description="Price without tax")
    price_taxed: Optional[float] = Field(None, ge=0, description="Price with tax")
    review_number: Optional[int] = Field(None, ge=0, description="Number of reviews")
    description: Optional[str] = Field(None, description="Book description")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Example Book",
                "genre_id": 1,
                "note": 4,
                "stock_number": 10,
                "price_taxed": 15.99,
                "description": "A great book"
            }
        }


class GenreDto(BaseModel):
    """
    DTO for genre data.
    This is what gets returned by the API.
    """
    id: int
    name: str = Field(..., min_length=1, description="Genre name")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Fiction"
            }
        }


class BookSearchRequestDto(BaseModel):
    """
    DTO for book search requests.
    """
    keyword: str = Field(..., min_length=1, description="Search keyword")

    class Config:
        json_schema_extra = {
            "example": {
                "keyword": "science"
            }
        }