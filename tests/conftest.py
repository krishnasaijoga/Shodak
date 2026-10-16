import pytest

from shodak.cache import cache
from shodak.llm.rate_limit import reset_provider_limiters
from shodak.usage import usage_tracker


@pytest.fixture(autouse=True)
def clear_shodak_cache():
    cache.clear()
    usage_tracker.reset()
    reset_provider_limiters()
    yield
    cache.clear()
    usage_tracker.reset()
    reset_provider_limiters()