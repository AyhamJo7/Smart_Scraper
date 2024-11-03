from typing import Any, Dict, List
import re
from urllib.parse import urlparse

class DataValidator:
    @staticmethod
    def validate_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    @staticmethod
    def clean_text(text: str) -> str:
        # Remove extra whitespace and normalize
        return " ".join(text.split())

    @staticmethod
    def validate_data_structure(data: Dict[str, Any], required_fields: List[str]) -> bool:
        return all(field in data for field in required_fields) 