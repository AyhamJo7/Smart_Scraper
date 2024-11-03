import pytest
from bs4 import BeautifulSoup
from ..src.utils.parsers import HTMLParser, DataParser

def test_html_parser():
    html = """
    <html>
        <title>Test Page</title>
        <body>
            <a href="https://example.com">Link</a>
        </body>
    </html>
    """
    
    parser = HTMLParser()
    soup = parser.parse_html(html)
    
    assert parser.extract_text(soup, "title") == "Test Page"
    assert len(parser.extract_links(soup)) == 1
    assert parser.extract_links(soup)[0] == "https://example.com"

def test_data_parser():
    json_str = '{"key": "value"}'
    parser = DataParser()
    
    result = parser.parse_json(json_str)
    assert result == {"key": "value"}
    
    invalid_json = "invalid json"
    result = parser.parse_json(invalid_json)
    assert result == {} 