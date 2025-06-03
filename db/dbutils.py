import time
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

def with_retry(
        func: Callable,
        max_retries: int = 3,
        initial_delay: float = 0.5,
        backoff_factor: float = 2,
        retryable_errors: tuple = (ConnectionError,),
        logger: logging.Logger = logger
) -> Callable:
    async def wrapper(*args, **kwargs):
        retries = 0
        delay = initial_delay

        while retries <= max_retries:
            try:
                return await func(*args, **kwargs)
            except retryable_errors as e:
                if retries >= max_retries:
                    logger.error(f"Retry exhausted after {max_retries} attempts")
                    raise RetryExhaustedError from e

                retries += 1
                logger.warning(
                    f"Retryable error: {str(e)}. "
                    f"Retrying in {delay:.2f}s (attempt {retries}/{max_retries})"
                )
                await asyncio.sleep(delay)
                delay *= backoff_factor
            except Exception as e:
                logger.error(f"Non-retryable error: {str(e)}")
                raise
    return wrapper