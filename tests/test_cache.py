from unittest.mock import patch

from shodak.cache import InMemoryCache, build_cache_key


def test_cache_key_is_deterministic():
    first=build_cache_key(
        "test",
        {
            "b":2,
            "a":1
        }
    )

    second=build_cache_key(
        "test",
        {
            "a":1,
            "b":2
        }
    )

    assert first==second


def test_cache_set_and_get():
    cache=InMemoryCache()

    cache.set(
        key="example",
        value="value",
        ttl_seconds=60
    )

    assert cache.get("example")=="value"


def test_expiry_cache_memory_is_removed():
    cache=InMemoryCache()

    with patch(
        "shodak.cache.time.time",
        return_value=100.0
    ):
        cache.set(
            key="example",
            value="value",
            ttl_seconds=10
        )
    with patch("shodak.cache.time.time",return_value=111.0):
        result=cache.get("example")
    assert result is None