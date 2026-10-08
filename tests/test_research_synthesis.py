from unittest.mock import MagicMock, patch

from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport
from shodak.models.research import ResearchRequest
from shodak.models.synthesis import ResearchSynthesis, SynthesizedFinding
from shodak.research.synthesis import synthesize_research


def test_llm_research_synthesis():
    report=ResearchReport(
        request=ResearchRequest(
            topic="retrieval augmented generation"
        ),
        research_questions=[],
        sources=[],
        evidence=[
                Evidence(
                claim="Retrieval can improve access to external knowledge.",
                supporting_text="Supporting evidence.",
                citation=Citation(
                    source_title="Example Paper",
                    source_url="https://example.com/paper"
                ),
                confidence=0.8
            )
        ],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=2,
            evidence_count=1,
            coverage_score=0.5
        )
    )
    structured_llm=MagicMock()

    structured_llm.invoke.return_value=ResearchSynthesis(
        key_findings=[
            SynthesizedFinding(
                finding="Retrieval can improve access to external knowledge.",
                supporting_evidence_indices=[0],
                confidence=0.0
            )
        ],
        uncertainties=[],
        contradictions=[],
        research_gaps=[],
        overall_confidence=0.8
    )

    base_llm=MagicMock()
    base_llm.with_structured_output.return_value=structured_llm

    expected_synthesis = ResearchSynthesis(
        key_findings=[
            SynthesizedFinding(
                finding="Retrieval can improve access to external knowledge.",
                supporting_evidence_indices=[0],
                confidence=0.8,
            )
        ],
        uncertainties=[],
        contradictions=[],
        research_gaps=[],
        overall_confidence=0.8,
    )

    with patch(
        "shodak.research.synthesis.invoke_structured_with_fallback",
        return_value=expected_synthesis,
    ):
        result=synthesize_research(report)

    assert len(result.key_findings)==1
    assert result.overall_confidence==0.8