from sqlalchemy import func
from sqlalchemy.orm import Session
from book_api.app.models import Book, Genre
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_books(db: Session):
    return db.query(Book).all()

def get_books_by_keyword(db: Session, keyword: str):
    return db.query(Book).filter(Book.title.ilike(f"%{keyword}%")).all()

def get_genres(db: Session):
    return db.query(Genre).all()

def get_books_by_genre(db: Session, genre_name: str):
    genre = db.query(Genre).filter(Genre.genre == genre_name).first()
    if genre:
        return db.query(Book).filter(Book.genre_id == genre.id).all()
    return []


