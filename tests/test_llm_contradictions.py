from unittest.mock import MagicMock, patch

from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.research.llm_contradictions import ContradictionResult, detect_contradiction_with_llm


def test_llm_detects_contradictions():
    first=Evidence(
        claim="Retrieval improves answer quality.",
        supporting_text="Evidence A.",
        citation=Citation(
            source_title="Paper One",
            source_url="https://example.com/1"
        ),
        confidence=0.8
    )
    second=Evidence(
            claim="Retrieval does not improve answer quality.",
            supporting_text="Evidence B.",
            citation=Citation(
                source_title="Paper Two",
                source_url="https://example.com/2"
            ),
            confidence=0.8
        )
    structured_llm=MagicMock()
    structured_llm.invoke.return_value=ContradictionResult(
        is_contradiction=True,
        explanation="The claims reach opposing conclusions."
    )

    base_llm=MagicMock()
    base_llm.with_structured_output.return_value=structured_llm

    with patch(
        "shodak.research.llm_contradictions.invoke_structured_with_fallback",
        return_value=ContradictionResult(
            is_contradiction=True,
            explanation="The two claims disagree about the effect.",
        ),
    ):
        result=detect_contradiction_with_llm(first,second)
    assert result is not None
    assert "disagree" in result.explanation.lower()