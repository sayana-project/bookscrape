"""
Main FastAPI application - Clean Architecture version.
This is the new entry point for your refactored API.
"""
from fastapi import FastAPI
from book_api.infrastructure.database.connection import engine, Base
from book_api.interface.api.book_router import router as book_router
from book_api.interface.api.genre_router import router as genre_router
from book_api.config.logging import setup_logging

# Setup logging
setup_logging(level="INFO")

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="BookScrape API - Clean Architecture",
    description="API pour livres et genres - Version refactorisée selon Clean Architecture",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(book_router)
app.include_router(genre_router)


@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint.
    """
    return {
        "message": "BookScrape API - Clean Architecture Version",
        "version": "2.0.0",
        "documentation": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "architecture": "clean"}