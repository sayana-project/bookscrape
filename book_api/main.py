from fastapi import FastAPI
from book_api.app.database import engine, Base
from book_api.app.router import router

# Création des tables
Base.metadata.create_all(bind=engine)

# Initialisation de l'application FastAPI
app = FastAPI(
    title="BookScrape API",
    prefix="/api",
    description="API pour livres et genres",
    version="1.0.0"
)

# Inclusion des routes
app.include_router(router)
