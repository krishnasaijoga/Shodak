from unittest.mock import MagicMock, patch

import pytest

from shodak.llm.retry import is_retryable_error, run_with_retry


def test_rate_limit_is_retryable():
    error=RuntimeError("429 Too Many Requests")
    assert is_retryable_error(error) is True


def test_validation_error_is_not_retryable():
    error=ValueError("Invalid schema configuration")
    assert is_retryable_error(error) is False


def test_operation_retries_then_succeeds():
    operation=MagicMock()

    operation.side_effect=[
        RuntimeError("429 Too Many Requests"),
        RuntimeError("Service Unavailable"),
        "success"
    ]

    with (patch("shodak.llm.retry.time.sleep")) as mock_sleep:
        result=run_with_retry(
            operation=operation,
            max_attempts=3,
            initial_delay=0.1,
            backoff_multiplier=2.0
        )

    assert result=="success"
    assert operation.call_count==3
    assert mock_sleep.call_count==2
    mock_sleep.assert_any_call(0.1)
    mock_sleep.assert_any_call(0.2)


def test_non_retryable_error_fails_immediately():
    operation=MagicMock()
    operation.side_effect=ValueError("Invalid API Key")

    with patch("shodak.llm.retry.time.sleep") as mock_sleep, pytest.raises(ValueError):
        run_with_retry(
            operation=operation,
            max_attempts=3
        )
    assert operation.call_count==1
    mock_sleep.assert_not_called()


def test_retryable_error_exhausts_attempts():
    operation=MagicMock()

    operation.side_effect=RuntimeError("Service Unavailable")

    with patch("shodak.llm.retry.time.sleep"), pytest.raises(RuntimeError):
        run_with_retry(
            operation=operation,
            max_attempts=3
        )
    assert operation.call_count==3