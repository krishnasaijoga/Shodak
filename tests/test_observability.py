import logging

import pytest

from shodak.observability import log_operation


def test_log_operation_success(caplog):
    with caplog.at_level(logging.INFO, logger="shodak"), log_operation("example_operation"):
        pass
    messages = [record.message for record in caplog.records]

    assert any("operation_started" in message for message in messages)

    assert any("operation_completed" in message for message in messages)


def test_log_operation_failure(caplog):
    with (
        caplog.at_level(logging.ERROR, logger="shodak"),
        pytest.raises(RuntimeError),
        log_operation("failing_operation"),
    ):
        raise RuntimeError("Test failure")
    messages = [record.message for record in caplog.records]

    assert any("operation_failed" in message for message in messages)
