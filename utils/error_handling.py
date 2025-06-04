from typing import TypeVar, Callable, Any
import asyncio
from functools import wraps
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')

class WorkflowError(Exception):
    """Base exception for workflow errors"""
    pass

class NodeExecutionError(WorkflowError):
    """Error during node execution"""
    pass

class RetryableError(WorkflowError):
    """Error that can be retried"""
    pass

def with_retry(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (RetryableError,)
) -> Callable:
    """Retry decorator for async functions"""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            current_delay = delay

            while True:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries > max_retries:
                        logger.error(f"Max retries ({max_retries}) exceeded: {str(e)}")
                        raise

                    logger.warning(
                        f"Retry {retries}/{max_retries} after error: {str(e)}. "
                        f"Waiting {current_delay}s"
                    )
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator
