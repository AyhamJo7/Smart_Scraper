import psutil
import asyncio
from loguru import logger

class ResourceManager:
    def __init__(self, max_memory_percent=80, max_cpu_percent=90):
        self.max_memory_percent = max_memory_percent
        self.max_cpu_percent = max_cpu_percent

    async def monitor_resources(self):
        while True:
            memory_percent = psutil.virtual_memory().percent
            cpu_percent = psutil.cpu_percent()

            if memory_percent > self.max_memory_percent:
                logger.warning(f"High memory usage: {memory_percent}%")

            if cpu_percent > self.max_cpu_percent:
                logger.warning(f"High CPU usage: {cpu_percent}%")

            await asyncio.sleep(60)  # Check every minute 