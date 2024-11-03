import pytest
import asyncio
from ..src.scraper.async_scraper import AsyncScraper
from ..src.scraper.headless_browser import HeadlessBrowser

@pytest.mark.asyncio
async def test_scraper_initialization():
    scraper = await AsyncScraper.initialize()
    assert scraper is not None
    await AsyncScraper.cleanup()

@pytest.mark.asyncio
async def test_scrape_url():
    scraper = await AsyncScraper.initialize()
    result = await scraper.scrape_url("https://example.com")
    
    assert "title" in result
    assert "links" in result
    assert "structured_data" in result
    
    await AsyncScraper.cleanup()

@pytest.mark.asyncio
async def test_headless_browser():
    browser = HeadlessBrowser()
    await browser.initialize()
    
    result = await browser.navigate("https://example.com")
    assert result["success"] is True
    assert "content" in result
    
    await browser.cleanup() 