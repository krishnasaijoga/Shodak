from unittest.mock import patch

from shodak.evaluation.scorecard import EvaluationScorecard
from shodak.models.citation import Citation
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport, ResearchRequest
from shodak.models.writing import OutputType
from shodak.writing.revision import RevisedDraft, RevisedSection, revise_draft_with_llm


def test_llm_revision_generates_structured_draft():
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

    scorecard = EvaluationScorecard(
        grounding_score=0.5,
        citation_correctness_score=0.5,
        hallucination_safety_score=0.5,
        style_similarity_score=0.8,
        format_compliance_score=0.8,
        research_quality_score=0.8,
        overall_quality_score=0.65,
    )
    original_draft = WritingDraft(
        output_type=OutputType.blog,
        title="Old Draft",
        sections=[
            DraftSection(
                heading="Introduction",
                content="Unsupported content.",
                citations=[],
            )
        ]
    )

    with patch(
        "shodak.writing.revision.invoke_structured_with_fallback",
        return_value=RevisedDraft(
            title="Understanding RAG",
            sections=[
                RevisedSection(
                    heading="Introduction",
                    content="Retrieval improves access to external knowledge."
                )
            ]
        )
    ):
        draft=revise_draft_with_llm(
            draft=original_draft,
            report=report,
            scorecard=scorecard
        )
    assert draft.title=="Understanding RAG"
    assert len(draft.sections)==1
    assert len(draft.sections[0].citations)==1
    assert draft.sections[0].heading=="Introduction"