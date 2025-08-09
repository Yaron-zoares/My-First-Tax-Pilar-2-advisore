"""
Logging configuration for Pilar2
"""

import logging
import sys
from pathlib import Path
from config.settings import settings

def setup_logging():
    """Setup logging configuration"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create logger
    logger = logging.getLogger("pilar2")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    return logger

def get_logger(name: str = "pilar2"):
    """Get a logger instance"""
    return logging.getLogger(name)
