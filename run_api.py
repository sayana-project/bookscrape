import uvicorn
import logging

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    uvicorn.run(
        "book_api.main:app",
        host="0.0.0.0",
        port=8010,
        reload=True,
        log_level="info"
    )