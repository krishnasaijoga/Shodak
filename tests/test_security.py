import pytest

from shodak.security import redact_secrets, safe_error_message, validate_output_path, validate_topic


def test_validate_topic_strips_whitespace():
    result=validate_topic("   retrieval augmented generation   ")
    assert result=="retrieval augmented generation"


def test_empty_topic_rejected():
    with pytest.raises(ValueError):
        validate_topic("    ")


def test_long_topic_rejected():
    with pytest.raises(ValueError):
        validate_topic("a"*501)


def test_openai_key_is_redacted():
    value="provider failed with sk-qwertyuiopasdfg"

    result=redact_secrets(value)

    assert "sk-" not in result
    assert "[REDACTED]" in result


def test_groq_key_is_redacted():
    value="gsk-asdfghjklzxcvbnm"

    result=redact_secrets(value)

    assert "gsk-" not in result
    assert "[REDACTED]" in result


def test_safe_error_message_is_bounded():
    exc=RuntimeError("x"*1000)
    result=safe_error_message(exc)
    assert len(result)<=503


def test_markdown_output_path_allowed():
    path=validate_output_path("output.md")
    assert path.suffix==".md"


def test_json_output_path_allowed():
    path=validate_output_path("output.json")
    assert path.suffix==".json"


def test_unsupported_output_path_rejected():
    with pytest.raises(ValueError):
        validate_output_path("output.exe")