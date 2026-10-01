from unittest.mock import patch

import pytest

from shodak.llm.factory import get_llm


def test_groq_requires_api_key():
    with (
        patch(
            "shodak.llm.factory.settings.llm_provider",
            "groq"
        ),
        patch(
        "shodak.llm.factory.settings.groq_api_key",
        None
        ), pytest.raises(
        ValueError,
        match="GROQ_API_KEY"
    )
    ):
        get_llm()


def test_openai_requires_api_key():
    with (
            patch(
                "shodak.llm.factory.settings.llm_provider",
                "openai"
            ),
            patch(
            "shodak.llm.factory.settings.openai_api_key",
            None
            ), pytest.raises(
        ValueError,
        match="OPENAI_API_KEY"
    )
        ):
        get_llm()


def test_unknown_provider_is_rejected():
     with patch(
          "shodak.llm.factory.settings.llm_provider",
          "unknown"
     ), pytest.raises(
          ValueError,
          match="Unsupported LLM provider"
     ):
         get_llm()