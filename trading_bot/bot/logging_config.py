"""Logging configuration for the trading bot."""
import logging
import os
from datetime import datetime

def setup_logging(log_dir="logs"):
    """
    Configure logging for the trading bot.
    
    Args:
        log_dir: Directory to store log files
    
    Returns:
        logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler - all logs
    log_filename = os.path.join(log_dir, f"trading_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Console handler - INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(detailed_formatter)
    logger.addHandler(console_handler)
    
    logger.info(f"Logging initialized. Log file: {log_filename}")
    
    return logger
