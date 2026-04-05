import logging
from logging.handlers import RotatingFileHandler
from core.config import Config
import os

def setup_logger():
    """
    Configure un logger global pour CyberGuard.
    - Logs dans un fichier rotatif
    - Logs dans la console
    """

    Config.ensure_directories()

    logger = logging.getLogger("CyberGuard")
    logger.setLevel(Config.LOG_LEVEL)

    # Empêcher la duplication des handlers
    if logger.handlers:
        return logger

    # Format des logs
    formatter = logging.Formatter(
        "%(asctime)s — %(levelname)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler fichier (rotatif)
    file_handler = RotatingFileHandler(
        Config.LOG_PATH,
        maxBytes=2_000_000,  # 2 MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# Logger global utilisable partout
logger = setup_logger()