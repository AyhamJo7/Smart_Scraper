import sys
from loguru import logger
from pathlib import Path
from ..config import load_config

def setup_logger():
    config = load_config()
    
    # Remove default logger
    logger.remove()
    
    # Add console logger
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level=config.LOG_LEVEL
    )
    
    # Add file logger
    log_file = Path(config.LOG_FILE)
    logger.add(
        log_file,
        rotation="500 MB",
        retention="10 days",
        compression="zip"
    ) 