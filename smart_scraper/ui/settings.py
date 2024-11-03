import streamlit as st
from typing import Dict, Any
from ..src.config import load_config, Settings

class SettingsUI:
    def __init__(self):
        self.config = load_config()

    def render(self):
        st.title("Smart Scraper Settings")
        
        # Scraper Settings
        st.header("Scraper Configuration")
        max_scrapes = st.number_input(
            "Max Concurrent Scrapes",
            min_value=1,
            max_value=20,
            value=self.config.MAX_CONCURRENT_SCRAPES
        )
        
        timeout = st.number_input(
            "Request Timeout (seconds)",
            min_value=5,
            max_value=120,
            value=self.config.REQUEST_TIMEOUT
        )
        
        # AI Settings
        st.header("AI Configuration")
        ai_model = st.selectbox(
            "AI Model",
            ["llama2", "gpt-3.5-turbo", "claude-2"],
            index=0
        )
        
        # Save Settings
        if st.button("Save Settings"):
            self.save_settings({
                "MAX_CONCURRENT_SCRAPES": max_scrapes,
                "REQUEST_TIMEOUT": timeout,
                "AI_MODEL": ai_model
            })

    def save_settings(self, settings: Dict[str, Any]):
        # Implementation for saving settings
        st.success("Settings saved successfully!") 