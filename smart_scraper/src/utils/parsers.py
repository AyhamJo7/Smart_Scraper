from bs4 import BeautifulSoup
from typing import Dict, Any, List
import json

class HTMLParser:
    @staticmethod
    def parse_html(html_content: str) -> BeautifulSoup:
        return BeautifulSoup(html_content, 'html.parser')

    @staticmethod
    def extract_text(soup: BeautifulSoup, selector: str) -> str:
        element = soup.select_one(selector)
        return element.text.strip() if element else ""

    @staticmethod
    def extract_links(soup: BeautifulSoup) -> List[str]:
        return [a.get('href') for a in soup.find_all('a', href=True)]

class DataParser:
    @staticmethod
    def parse_json(content: str) -> Dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def extract_structured_data(soup: BeautifulSoup) -> List[Dict[str, Any]]:
        data = []
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data.append(json.loads(script.string))
            except json.JSONDecodeError:
                continue
        return data 