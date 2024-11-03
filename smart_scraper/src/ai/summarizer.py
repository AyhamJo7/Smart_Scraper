from .ollama_integration import OllamaClient

class TextSummarizer:
    def __init__(self):
        self.ollama_client = OllamaClient()

    async def summarize(self, text: str, max_length: int = 200) -> str:
        prompt = f"""Summarize the following text in a concise way 
        (maximum {max_length} characters):
        
        {text}
        """
        return await self.ollama_client.generate(prompt)

    async def bullet_points(self, text: str, num_points: int = 5) -> list:
        prompt = f"""Extract the {num_points} most important points from this text:
        
        {text}
        """
        response = await self.ollama_client.generate(prompt)
        return response.split('\n') 