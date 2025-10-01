"""
SQLAlchemy database models.
These are the database table definitions.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from book_api.infrastructure.database.connection import Base


class BookModel(Base):
    """
    SQLAlchemy model for books table.
    This represents the database table structure.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    genre_id = Column(Integer, ForeignKey("books_genres.id"))
    note = Column(Integer)
    stock_number = Column(Integer)
    datetime = Column(String)
    upc = Column(String)
    product_type = Column(String)
    price_ht = Column(Float)
    price_taxed = Column(Float)
    review_number = Column(Integer)
    description = Column(String)


class GenreModel(Base):
    """
    SQLAlchemy model for genres table.
    This represents the database table structure.
    """
    __tablename__ = "books_genres"

    id = Column(Integer, primary_key=True, index=True)
    genre = Column(String, unique=True, index=True)