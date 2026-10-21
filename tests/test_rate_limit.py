import threading
from unittest.mock import patch

import pytest

from shodak.llm.rate_limit import ProviderRateLimiter, get_provider_limiter, reset_provider_limiters


def test_invalid_min_interval():
    with pytest.raises(ValueError):
        ProviderRateLimiter(min_interval_seconds=-1)


def test_same_provider_reuses_limiter():
    reset_provider_limiters()

    first = get_provider_limiter("groq", max_concurrent=3, min_interval_seconds=0.0)

    second = get_provider_limiter("groq", max_concurrent=3, min_interval_seconds=0.0)

    assert first is second


def test_different_providers_get_different_limiters():
    reset_provider_limiters()

    groq = get_provider_limiter("groq", max_concurrent=3, min_interval_seconds=0.0)

    openai = get_provider_limiter("openai", max_concurrent=3, min_interval_seconds=0.0)

    assert groq is not openai


def test_rate_limiter_waits_when_needed():
    limiter = ProviderRateLimiter(max_concurrent=1, min_interval_seconds=1.0)

    with (
        patch("shodak.llm.rate_limit.time.monotonic", side_effect=[10.0, 10.0, 10.2, 11.0]),
        patch("shodak.llm.rate_limit.time.sleep") as mock_sleep,
    ):
        with limiter.acquire():
            pass

        with limiter.acquire():
            pass

    mock_sleep.assert_called_once()
    waited = mock_sleep.call_args.args[0]
    assert waited == pytest.approx(0.8)


def test_concurrency_is_limited():
    limiter = ProviderRateLimiter(max_concurrent=1)

    first_entered = threading.Event()
    allow_first_to_exit = threading.Event()
    second_entered = threading.Event()

    def first_worker():
        with limiter.acquire():
            first_entered.set()

            allow_first_to_exit.wait(timeout=1)

    def second_worker():
        first_entered.wait(timeout=1)

        with limiter.acquire():
            second_entered.set()

    first_thread = threading.Thread(target=first_worker)

    second_thread = threading.Thread(target=second_worker)

    first_thread.start()
    second_thread.start()

    assert first_entered.wait(timeout=1)

    assert second_entered.wait(timeout=0.05) is False

    allow_first_to_exit.set()

    assert second_entered.wait(timeout=1)

    first_thread.join()
    second_thread.join()
