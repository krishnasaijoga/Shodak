import pytest
from pydantic import ValidationError

from shodak.config import Settings


def test_invalid_max_attempts_rejected():
    with pytest.raises(ValidationError):
        Settings(llm_max_attempts=0)


def test_negative_retry_delay_rejected():
    with pytest.raises(ValidationError):
        Settings(llm_retry_initial_delay=-1)


def test_invalid_provider_rejected():
    with pytest.raises(ValidationError):
        Settings(llm_provider="invalid")