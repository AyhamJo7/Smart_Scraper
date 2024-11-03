from playwright.async_api import async_playwright, Browser, Page
from typing import Optional, Dict, Any
from loguru import logger

class HeadlessBrowser:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def initialize(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()

    async def navigate(self, url: str) -> Dict[str, Any]:
        try:
            await self.page.goto(url, wait_until='networkidle')
            return {
                'success': True,
                'content': await self.page.content(),
                'screenshot': await self.page.screenshot(full_page=True)
            }
        except Exception as e:
            logger.error(f"Navigation error: {str(e)}")
            return {'success': False, 'error': str(e)}

    async def cleanup(self):
        if self.browser:
            await self.browser.close() 