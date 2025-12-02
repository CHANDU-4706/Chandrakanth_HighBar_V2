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
        if hasattr(record, "decision_data"):
            log_record["decision"] = record.decision_data
            
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

class LoggerWrapper(logging.Logger):
    def decision(self, agent_name: str, input_data: str, output_data: str, reason: str):
        """
        Log a decision made by an agent.
        """
        decision_data = {
            "agent": agent_name,
            "input_summary": input_data[:200] + "..." if len(input_data) > 200 else input_data,
            "output_summary": output_data[:200] + "..." if len(output_data) > 200 else output_data,
            "reason": reason
        }
        self._log(logging.INFO, f"Decision by {agent_name}: {reason}", (), extra={"decision_data": decision_data})

logging.setLoggerClass(LoggerWrapper)

def setup_logger(name="kasparro_app", log_dir="logs"):
    """
    Sets up a logger with console (INFO) and file (DEBUG/JSON) handlers.
    Creates a unique run folder.
    """
    # Create a unique run folder based on timestamp
    run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    run_dir = os.path.join(log_dir, run_id)
    os.makedirs(run_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent adding handlers multiple times
    if logger.hasHandlers():
        return logger, run_dir

    # Console Handler - Human readable
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File Handler - Machine readable (JSON)
    log_file = os.path.join(run_dir, "app.json")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)

    return logger, run_dir

# Global logger instance
# Note: We might need to re-initialize this in run.py to get the run_dir
logger, current_run_dir = setup_logger()
