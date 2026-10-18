import time
from collections.abc import Callable

from shodak.research.exceptions import ResearchConnectionError, ResearchRateLimitError


def run_research_with_retry[T](
        operation:Callable[[],T],
        *,
        max_attempts:int=3,
        initial_delay:float=1.0,
        backoff_multiplier:float=2.0
)->T:
    if max_attempts<1:
        raise ValueError("max_attempts must be at least 1.")
    delay=initial_delay
    last_error:Exception|None=None

    for attempt in range(1,max_attempts+1):
        try:
            return operation()
        except (
            ResearchRateLimitError,
            ResearchConnectionError
        ) as exc:
            last_error=exc

            if attempt==max_attempts:
                raise

            time.sleep(delay)

            delay*=backoff_multiplier
    raise RuntimeError("Research retry failed unexpectedly.") from last_error