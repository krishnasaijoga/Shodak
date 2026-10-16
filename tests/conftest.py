import pytest

from shodak.cache import cache
from shodak.usage import usage_tracker


@pytest.fixture(autouse=True)
def clear_shodak_cache():
    cache.clear()
    usage_tracker.reset()
    yield
    cache.clear()
    usage_tracker.reset()