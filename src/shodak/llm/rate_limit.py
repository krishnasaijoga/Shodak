import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager


class ProviderRateLimiter:
    def __init__(
            self,
            max_concurrent:int=3,
            min_interval_seconds:float=0.0
    )->None:
        if max_concurrent<1:
            raise ValueError("max concurrent must be at least 1.")

        if min_interval_seconds<0:
            raise ValueError("min_interval_seconds cannot be negative.")

        self._semaphore=threading.BoundedSemaphore(max_concurrent)

        self._lock=threading.Lock()

        self._min_interval_seconds=min_interval_seconds

        self._last_request_time=0.0


    def _wait_for_rate_limit(self)->None:
        with self._lock:
            now=time.monotonic()
            elapsed=now-self._last_request_time
            remaining=self._min_interval_seconds-elapsed

            if remaining>0:
                time.sleep(remaining)

            self._last_request_time=time.monotonic()

    @contextmanager
    def acquire(self)->Iterator[None]:
        with self._semaphore:
            self._wait_for_rate_limit()
            yield

_limiters:dict[str,ProviderRateLimiter]={}

_registry_lock=threading.Lock()

def get_provider_limiter(
        provider:str,
        *,
        max_concurrent:int,
        min_interval_seconds:float
)->ProviderRateLimiter:
    with _registry_lock:
        if provider not in _limiters:
            _limiters[provider]=ProviderRateLimiter(
                max_concurrent=max_concurrent,
                min_interval_seconds=min_interval_seconds
            )
        return _limiters[provider]


def reset_provider_limiters()->None:
    with _registry_lock:
        _limiters.clear()