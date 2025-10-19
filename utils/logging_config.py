"""
Logging configuration for the meme simulation.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logging(log_level: str = "INFO"):
    """
    Setup logging configuration with both file and console output.
    
    Args:
        log_level: Logging level ("DEBUG" or "INFO")
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create timestamped log filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"memesim_{timestamp}.log"
    
    # Convert log_level string to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture everything
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # File handler (gets everything at specified level)
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(numeric_level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler (INFO only for cleaner output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Log the startup
    logging.info(f"Logging initialized. Log file: {log_file}")
    logging.info(f"Log level: {log_level}")
    
    return log_file

