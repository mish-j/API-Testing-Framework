# api_client/logger.py
import logging
import os
from datetime import datetime

def setup_logger(log_level=logging.INFO, log_to_file=False):
    """
    Set up a logger for the API testing framework.
    
    Args:
        log_level (int): Logging level (default: INFO)
        log_to_file (bool): Whether to save logs to a file
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger("api_test_framework")
    logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_to_file:
        log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"api_test_{timestamp}.log")
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger