import functools
import traceback
import time
from typing import Any, Callable, Optional, Type
from .logger import logger

class AgentError(Exception):
    """Base exception for Agent failures."""
    pass

def safe_execute(
    default_return: Any = None,
    log_context: str = "Operation",
    raise_on_error: bool = False,
    retries: int = 0,
    backoff_factor: float = 1.0
):
    """
    Decorator to wrap a function with try-except block and retry logic.
    
    Args:
        default_return: Value to return if exception occurs after all retries.
        log_context: String to identify the operation in logs.
        raise_on_error: If True, re-raises the exception after logging (and retries).
        retries: Number of times to retry on failure.
        backoff_factor: Multiplier for sleep time between retries.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt <= retries:
                try:
                    logger.debug(f"Starting {log_context} (Attempt {attempt + 1}/{retries + 1})...")
                    result = func(*args, **kwargs)
                    logger.debug(f"Completed {log_context} successfully.")
                    return result
                except Exception as e:
                    error_msg = f"Error in {log_context} (Attempt {attempt + 1}): {str(e)}"
                    logger.warning(error_msg)
                    
                    if attempt < retries:
                        sleep_time = backoff_factor * (2 ** attempt)
                        logger.info(f"Retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
                        attempt += 1
                    else:
                        logger.error(f"Failed {log_context} after {retries + 1} attempts.")
                        logger.debug(traceback.format_exc())
                        
                        if raise_on_error:
                            raise AgentError(error_msg) from e
                        
                        return default_return
        return wrapper
    return decorator
