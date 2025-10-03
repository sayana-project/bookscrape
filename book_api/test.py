from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from book_api.app.models import Book, Genre

# Connexion à la base
DATABASE_URL = "sqlite:///app/books.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Session
db = SessionLocal()

books = db.query(Book).all()
print(" Livres trouvés :", len(books))
for book in books[:5]:
    print(f"- {book.title} (Genre ID: {book.genre_id})")

genres = db.query(Genre).all()
print("\n Genres trouvés :", len(genres))
for genre in genres:
    print(f"- {genre.id}: {genre.genre}")

target_genre = "Poetry"
genre_obj = db.query(Genre).filter(Genre.genre == target_genre).first()
if genre_obj:
    poetry_books = db.query(Book).filter(Book.genre_id == genre_obj.id).all()
    print(f"\n Livres en genre '{target_genre}':", len(poetry_books))
    for book in poetry_books:
        print(f"- {book.title}")
else:
    print(f"\n Genre '{target_genre}' non trouvé.")

db.close()
