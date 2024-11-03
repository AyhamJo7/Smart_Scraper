import streamlit as st
import plotly.express as px
from typing import List, Dict, Any
from ..src.scraper.async_scraper import AsyncScraper
from ..src.ai.content_analysis import ContentAnalyzer

class Dashboard:
    def __init__(self):
        self.scraper = None
        self.analyzer = ContentAnalyzer()
        
    async def initialize(self):
        self.scraper = await AsyncScraper.initialize()

    def render(self):
        st.title("Smart Scraper Dashboard")
        
        # Sidebar
        st.sidebar.header("Settings")
        analyze = st.sidebar.checkbox("Enable AI Analysis")
        
        # Main content
        urls = st.text_area("Enter URLs (one per line)")
        if st.button("Start Scraping"):
            urls_list = [url.strip() for url in urls.split("\n") if url.strip()]
            self.start_scraping(urls_list, analyze)

    async def start_scraping(self, urls: List[str], analyze: bool):
        with st.spinner("Scraping in progress..."):
            results = await self.scraper.scrape_multiple(urls)
            self.display_results(results, analyze)

    def display_results(self, results: List[Dict[str, Any]], analyze: bool):
        for idx, result in enumerate(results):
            st.subheader(f"Result {idx + 1}")
            if "error" in result:
                st.error(result["error"])
            else:
                st.success("Scraping successful")
                st.json(result)

def create_dashboard():
    dashboard = Dashboard()
    dashboard.render() 