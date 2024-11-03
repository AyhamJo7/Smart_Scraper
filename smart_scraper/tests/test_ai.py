import pytest
from ..src.ai.content_analysis import ContentAnalyzer
from ..src.ai.summarizer import TextSummarizer

@pytest.mark.asyncio
async def test_content_analyzer():
    analyzer = ContentAnalyzer()
    text = "Apple Inc. is planning to open a new store in New York City."
    
    analysis = await analyzer.analyze_text(text)
    assert isinstance(analysis, dict)
    
    entities = await analyzer.extract_entities(text)
    assert isinstance(entities, list)

@pytest.mark.asyncio
async def test_summarizer():
    summarizer = TextSummarizer()
    text = "This is a long text that needs to be summarized. " * 10
    
    summary = await summarizer.summarize(text, max_length=100)
    assert len(summary) <= 100
    
    points = await summarizer.bullet_points(text, num_points=3)
    assert len(points) <= 3 