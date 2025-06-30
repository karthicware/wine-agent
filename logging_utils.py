import logging
import sys

def setup_logger():
    """Set up the logger for the application."""
    logger = logging.getLogger("WineAgent")
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler("wine_agent.log")
    file_handler.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add handlers to the logger
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

logger = setup_logger() 