from playwright.async_api import async_playwright
from typing import List, Dict, Any
import asyncio
from loguru import logger
from ..config import load_config
from ..utils.parsers import HTMLParser, DataParser

class AsyncScraper:
    _instance = None
    _browser = None
    _context = None

    @classmethod
    async def initialize(cls):
        if not cls._instance:
            cls._instance = cls()
            playwright = await async_playwright().start()
            cls._browser = await playwright.chromium.launch()
            cls._context = await cls._browser.new_context()
        return cls._instance

    @classmethod
    async def cleanup(cls):
        if cls._browser:
            await cls._browser.close()

    async def scrape_url(self, url: str) -> Dict[str, Any]:
        try:
            page = await self._context.new_page()
            await page.goto(url)
            content = await page.content()
            
            parser = HTMLParser()
            soup = parser.parse_html(content)
            
            data = {
                "title": parser.extract_text(soup, "title"),
                "links": parser.extract_links(soup),
                "structured_data": DataParser.extract_structured_data(soup)
            }
            
            await page.close()
            return data
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return {"error": str(e)}

    async def scrape_multiple(self, urls: List[str]) -> List[Dict[str, Any]]:
        config = load_config()
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_SCRAPES)
        
        async def scrape_with_semaphore(url: str) -> Dict[str, Any]:
            async with semaphore:
                return await self.scrape_url(url)
        
        tasks = [scrape_with_semaphore(url) for url in urls]
        return await asyncio.gather(*tasks) 