import logging
import sys
import json
import os
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after parsing the LogRecord.
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineNo": record.lineno
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def setup_logger(name="kasparro_app", log_dir="logs"):
    """
    Sets up a logger with console (INFO) and file (DEBUG/JSON) handlers.
    """
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent adding handlers multiple times
    if logger.hasHandlers():
        return logger

    # Console Handler - Human readable
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File Handler - Machine readable (JSON)
    log_file = os.path.join(log_dir, "app.json")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)

    return logger

# Global logger instance
logger = setup_logger()
