import asyncio
from fastapi import FastAPI
from loguru import logger
from config import load_config
from api.endpoints import router as api_router
from scraper.async_scraper import AsyncScraper
from ui.dashboard import create_dashboard

app = FastAPI(title="Smart Scraper", version="1.0.0")
app.include_router(api_router, prefix="/api")

def init_logger():
    config = load_config()
    logger.add(
        config.LOG_FILE,
        level=config.LOG_LEVEL,
        rotation="500 MB",
    )

async def startup():
    init_logger()
    logger.info("Starting Smart Scraper...")
    await AsyncScraper.initialize()

async def shutdown():
    logger.info("Shutting down Smart Scraper...")
    await AsyncScraper.cleanup()

app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

if __name__ == "__main__":
    import uvicorn
    create_dashboard()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 