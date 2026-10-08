from unittest.mock import MagicMock, patch

from pydantic import BaseModel

from shodak.llm.router import invoke_structured_with_fallback


class ExampleOutput(BaseModel):
    value:str


def test_primary_provider_succeeds():
    primary_llm=MagicMock()
    structured_llm=MagicMock()
    structured_llm.invoke.return_value=ExampleOutput(value="primary")
    primary_llm.with_structured_output.return_value=(structured_llm)

    with patch(
        "shodak.llm.router.get_llm_candidates",
        return_value=[('groq',primary_llm)]
    ):
        result=invoke_structured_with_fallback(
            schema=ExampleOutput,
            prompt="Test Prompt"
        )
    assert result.value=="primary"


def test_fallback_provider_is_used():
    primary_llm=MagicMock()
    fallback_llm=MagicMock()

    primary_structured=MagicMock()
    primary_structured.invoke.side_effect=RuntimeError("Primary provider failed.")
    fallback_structured=MagicMock()
    fallback_structured.invoke.return_value=ExampleOutput(value='fallback')

    primary_llm.with_structured_output.return_value=(primary_structured)

    fallback_llm.with_structured_output.return_value=(fallback_structured)

    with patch(
        "shodak.llm.router.get_llm_candidates",
        return_value=[
            ('groq',primary_llm),
            ('openai',fallback_llm)
        ]
    ):
        result=invoke_structured_with_fallback(
            schema=ExampleOutput,
            prompt="Test prompt"
        )
    assert result.value=="fallback"



def test_all_proiders_fail():
    first_llm=MagicMock()
    second_llm=MagicMock()

    first_structured=MagicMock()
    second_structured=MagicMock()

    first_structured.invoke.side_effect=RuntimeError("First failed.")
    second_structured.invoke.side_effect=RuntimeError("Second failed.")

    first_llm.with_structured_output.return_value=(
        first_structured
    )
    second_llm.with_structured_output.return_value=(
        second_structured
    )

    with patch(
        "shodak.llm.router.get_llm_candidates",
        return_value=[
            ('groq',first_llm),
            ('openai',second_llm)
        ]
    ):
        try:
            invoke_structured_with_fallback(schema=ExampleOutput,prompt="Test prompt.")
        except RuntimeError as exc:
            assert "All configured LLM providers failed" in str(exc)
        else:
            raise AssertionError("Expected RuntimeError")