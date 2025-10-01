from book_api.app.database import SessionLocal
from book_api.app.models import Genre

db = SessionLocal()
genres = db.query(Genre).all()

for genre in genres:
    print(f"{genre.id} - {genre.genre}")
