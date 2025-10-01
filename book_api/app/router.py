from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from book_api.app.models import Book, Genre
from book_api.app.database import SessionLocal
from book_api.app.schemas import BookSchema, GenreSchema
from book_api.app.crud import get_books_by_keyword,get_books, get_genres, get_books_by_genre
router = APIRouter()

# Dependency pour la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/books", response_model=List[BookSchema], tags=["Books"], summary="Get all books")
def read_books(db: Session = Depends(get_db)):
    return get_books(db)

@router.get("/books/{keyword}", response_model=List[BookSchema], tags=["Books"], summary="Get books containing keyword")
def read_books_by_keyword(keyword: str, db: Session = Depends(get_db)):
    return get_books_by_keyword(db, keyword)

@router.get("/genres", response_model=List[GenreSchema], tags=["Genres"], summary="Get all genres")
def read_genres(db: Session = Depends(get_db)):
    return get_genres(db)

@router.get("/books/by_genre/{genre_name}", response_model=List[BookSchema], tags=["Books"], summary="Get books by genre")
def read_books_by_genre(genre_name: str, db: Session = Depends(get_db)):
    return get_books_by_genre(db, genre_name)

@router.get("/books/average_price/all", tags=["Books"])
def average_price_all_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    prices = [b.price_taxed for b in books if b.price_taxed is not None]
    avg = round(sum(prices) / len(prices), 2) if prices else 0.0
    logger.info(f"Moyenne calculée sur {len(prices)} livres valides parmi {len(books)}")
    return {
        "total_books": len(books),
        "books_with_price": len(prices),
        "average_price": avg,
    }

@router.get("/books/average_price/genre/{genre_id}", tags=["Genres"], summary="Get books average price by genre")
def average_price_by_genre(genre_id: int, db: Session = Depends(get_db)):
    # Récupère le genre
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre introuvable")

    # Récupère tous les livres du genre
    books = db.query(Book).filter(Book.genre_id == genre_id).all()

    # Extrait les prix valides
    prices = [b.price_taxed for b in books if b.price_taxed is not None]

    # Calcule la moyenne manuellement
    avg = round(sum(prices) / len(prices), 2) if prices else 0.0

    logger.info(f"Genre {genre.genre} ({genre_id}) → {len(prices)} prix valides sur {len(books)} livres")

    return {
        "genre_id": genre_id,
        "genre_name": genre.genre,
        "total_books": len(books),
        "books_with_price": len(prices),
        "average_price": avg,
        "sample_prices": prices[:10]
    }


@router.get("/books/debug", tags=["Debug"])
def debug(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return {"count": len(books)}

@router.get("/books/debug", response_model=List[BookSchema])
def debug_books(db: Session = Depends(get_db)):
    return db.query(Book).limit(5).all()


@router.get("/books/average_stock/all", tags=["Books"])
def average_stock_all_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    stock_numbers = [b.stock_number for b in books if b.stock_number is not None]
    avg = round(sum(stock_numbers) / len(stock_numbers), 0) if stock_numbers else 0
    logger.info(f"Moyenne calculée sur {len(stock_numbers)} livres valides parmi {len(books)}")
    return {
        "total_books": len(books),
        "books_with_stock": len(stock_numbers),
        "average_stock": avg,
    }

@router.get("/books/average_stock/genre/{genre_id}", tags=["Genres"], summary="Get books average stock by genre")
def average_stock_by_genre(genre_id: int, db: Session = Depends(get_db)):
    # Récupère le genre
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre introuvable")

    # Récupère tous les livres du genre
    books = db.query(Book).filter(Book.genre_id == genre_id).all()

    # Extrait les stocks valides
    stock_numbers = [b.stock_number for b in books if b.stock_number is not None]

    # Calcule la moyenne manuellement
    avg = round(sum(stock_numbers) / len(stock_numbers), 0) if stock_numbers else 0

    logger.info(f"Genre {genre.genre} ({genre_id}) → {len(stock_numbers)} stocks valides sur {len(books)} livres")

    return {
        "genre_id": genre_id,
        "genre_name": genre.genre,
        "total_books": len(books),
        "books_with_stock": len(stock_numbers),
        "average_stock": avg,
        "sample_stocks": stock_numbers[:10]
    }

@router.get("/books/stock/by_title/{title}", tags=["Books"], summary="Get stock values by title")
def stock_by_title(title: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.title.ilike(f"%{title}%")).all()
    stocks = [b.stock_number for b in books if b.stock_number is not None]

    logger.info(f"Title '{title}' → {len(stocks)} stocks extraits sur {len(books)} livres")

    return {
        "title_query": title,
        "total_books": len(books),
        "books_with_stock": len(stocks),
        "stock_values": stocks
    }

@router.get("/books/stock/by_upc/{upc}", tags=["Books"], summary="Get stock values by UPC")
def stock_by_upc(upc: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.upc.ilike(f"%{upc}%")).all()
    stocks = [b.stock_number for b in books if b.stock_number is not None]

    logger.info(f"UPC '{upc}' → {len(stocks)} stocks extraits sur {len(books)} livres")

    return {
        "upc_query": upc,
        "total_books": len(books),
        "books_with_stock": len(stocks),
        "stock_values": stocks
    }

@router.get("/books/stock/by_id/{book_id}", tags=["Books"], summary="Get stock value by book ID")
def stock_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livre introuvable")

    stock = book.stock_number if book.stock_number is not None else 0

    logger.info(f"Book ID {book_id} → stock = {stock}")

    return {
        "book_id": book_id,
        "title": book.title,
        "upc": book.upc,
        "stock_number": stock
    }
