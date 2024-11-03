import aiohttp
from typing import Dict, Any
import json
from loguru import logger
from ..config import load_config

class OllamaClient:
    def __init__(self):
        self.config = load_config()
        self.base_url = self.config.OLLAMA_API_URL
        self.model = self.config.AI_MODEL

    async def generate(self, prompt: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('response', '')
                else:
                    logger.error(f"Ollama API error: {response.status}")
                    return ""

    async def analyze_content(self, content: str) -> Dict[str, Any]:
        prompt = f"Analyze the following content and extract key information:\n\n{content}"
        response = await self.generate(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI response"} 