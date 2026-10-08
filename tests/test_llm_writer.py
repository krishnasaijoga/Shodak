from unittest.mock import MagicMock, patch

from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport, ResearchRequest
from shodak.models.synthesis import ResearchSynthesis, SynthesizedFinding
from shodak.models.writing import OutputType, WritingRequest
from shodak.writing.llm_writer import GeneratedDraft, GeneratedSection, generate_draft_with_llm


def test_llm_writer_generates_structured_draft():
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
            evidence_count=2,
            coverage_score=0.5
        )
    )

    synthesis=ResearchSynthesis(
            key_findings=[
                SynthesizedFinding(
                    finding="Retrieval can improve access to external knowledge.",
                    supporting_evidence_indices=[0],
                    confidence=0.8
                )
            ],
            uncertainties=["Effectiveness depends on retrieval quality."],
            contradictions=[],
            research_gaps=[],
            overall_confidence=0.8
    )

    request=WritingRequest(
        output_type=OutputType.blog
    )

    structured_llm=MagicMock()
    structured_llm.invoke.return_value=GeneratedDraft(
        title="Understanding Retrieval Augmented Generation",
        sections=[
            GeneratedSection(
                heading="Introduction",
                content="Retrieval augmented generation connects models with external knowledge."
            ),
            GeneratedSection(
                heading="Conclusion",
                content="Its effectiveness still depends heavily on retrieval quality."
            )
        ]
    )

    base_llm=MagicMock()
    base_llm.with_structured_output.return_value=structured_llm

    with patch(
        "shodak.writing.llm_writer.get_llm",
        return_value=base_llm
    ):
        draft=generate_draft_with_llm(
            report=report,
            request=request,
            research_synthesis=synthesis
        )
    assert draft.title=="Understanding Retrieval Augmented Generation"
    assert len(draft.sections)==2
    assert draft.sections[0].heading=="Introduction"