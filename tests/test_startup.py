from unittest.mock import patch

from shodak.startup import validate_filesystem_configuration, validate_provider_configuration


def test_no_provider_is_unhealthy():
    with (
        patch("shodak.startup.settings.groq_api_key", None),
        patch("shodak.startup.settings.openai_api_key", None),
    ):
        result = validate_provider_configuration()

    assert result.healthy is False
    assert result.errors


def test_fallback_only_is_healthy_with_warning():
    with (
        patch("shodak.startup.settings.llm_provider", "groq"),
        patch("shodak.startup.settings.groq_api_key", None),
        patch("shodak.startup.settings.openai_api_key", "test-key"),
    ):
        result = validate_provider_configuration()

    assert result.healthy is True
    assert result.warnings


def test_valid_history_directory(tmp_path):
    history = tmp_path / "history" / "runs.jsonl"

    with (
        patch("shodak.startup.settings.run_history_enabled", True),
        patch("shodak.startup.settings.run_history_path", str(history)),
    ):
        result = validate_filesystem_configuration()

    assert result.healthy is True
    assert history.parent.exists()
