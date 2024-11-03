from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any
from ..scraper.async_scraper import AsyncScraper
from ..ai.content_analysis import ContentAnalyzer

router = APIRouter()

class ScrapeRequest(BaseModel):
    urls: List[HttpUrl]
    analyze: bool = False

class ScrapeResponse(BaseModel):
    results: List[Dict[str, Any]]

@router.post("/scrape", response_model=ScrapeResponse)
async def scrape_urls(request: ScrapeRequest):
    scraper = await AsyncScraper.initialize()
    analyzer = ContentAnalyzer() if request.analyze else None
    
    results = await scraper.scrape_multiple(request.urls)
    
    if request.analyze:
        for result in results:
            if 'error' not in result:
                analysis = await analyzer.analyze_text(result.get('content', ''))
                result['analysis'] = analysis
    
    return ScrapeResponse(results=results) 