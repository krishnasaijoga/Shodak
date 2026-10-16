import time
from collections.abc import Callable

RETRYABLE_MESSAGES={
    "429",
    "rate limit",
    "too many requests",
    "timeout",
    "timed out",
    "temporarily unavailable",
    "service unavailable",
    "connection error",
    "connection reset"
}


def is_retryable_error(exc:Exception)->bool:
    message=str(exc).lower()
    return any(item in message for item in RETRYABLE_MESSAGES)


def run_with_retry[T](
        operation:Callable[[],T],
        max_attempts:int=3,
        initial_delay:float=0.5,
        backoff_multiplier:float=2.0
)->T:
    if max_attempts<1:
        raise ValueError("max_attempts must be at least 1.")
    delay=initial_delay
    last_error:Exception | None=None

    for attempt in range(1,max_attempts+1):
        try:
            return operation()
        except Exception as exc:
            last_error=exc
            if not is_retryable_error(exc) or attempt==max_attempts:
                raise
        time.sleep(delay)
        delay*=backoff_multiplier
    raise RuntimeError("Retry operation failed unexpectedly.") from last_error