import functools
import traceback
import time
from typing import Any, Callable, Optional, Type
from src.utils.logger import logger

class AgentError(Exception):
    """Base exception for Agent failures."""
    pass

class SchemaValidationError(AgentError):
    """Raised when data does not match the expected schema."""
    pass

class DataProcessingError(AgentError):
    """Raised when data processing fails (e.g., calculation errors)."""
    pass

class AgentExecutionError(AgentError):
    """Raised when an agent fails to execute its task."""
    pass

def safe_execute(
    default_return: Any = None,
    log_context: str = "Operation",
    raise_on_error: bool = False,
    retries: int = 0,
    backoff_factor: float = 1.0,
    allowed_exceptions: tuple = ()
):
    """
    Decorator to wrap a function with try-except block and retry logic.
    
    Args:
        default_return: Value to return if exception occurs after all retries.
        log_context: String to identify the operation in logs.
        raise_on_error: If True, re-raises the exception after logging (and retries).
        retries: Number of times to retry on failure.
        backoff_factor: Multiplier for sleep time between retries.
        allowed_exceptions: Tuple of exceptions that should NOT trigger a retry (fail fast).
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
                except allowed_exceptions as e:
                    logger.error(f"Critical error in {log_context}: {str(e)} (No Retry)")
                    if raise_on_error:
                        raise e
                    return default_return
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
                            # If it's already one of our custom errors, re-raise it.
                            # Otherwise, wrap it in AgentExecutionError
                            if isinstance(e, AgentError):
                                raise e
                            raise AgentExecutionError(error_msg) from e
                        
                        return default_return
        return wrapper
    return decorator
