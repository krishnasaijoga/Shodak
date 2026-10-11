from shodak.evaluation.scorecard import evaluate_output
from shodak.models.citation import Citation
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport, ResearchRequest
from shodak.models.source import Source, SourceProvider, SourceType
from shodak.models.writing import OutputType


def test_combined_evaluation_scorecard():
    citation=Citation(
        source_title="RAG Paper",
        source_url="https://example.com/rag"
    )
    evidence=Evidence(
        claim="Retrieval improves access to external knowledge.",
        supporting_text="Supporting evidence.",
        citation=citation,
        confidence=0.9
    )
    source=Source(
        title="RAG Paper",
        url="https://example.com/rag",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref
    )
    report=ResearchReport(
        request=ResearchRequest(
            topic="retrieval augmented generation"
        ),
        research_questions=[],
        sources=[source],
        evidence=[evidence],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=1,
            evidence_count=1,
            coverage_score=0.8,
        )
    )
    draft=WritingDraft(
        output_type=OutputType.blog,
        title="Understanding RAG",
        sections=[
            DraftSection(
                heading="Introduction",
                content=(
                    "Retrieval improves access "
                    "to external knowledge."
                ),
                citations=[citation],
            ),
            DraftSection(
                heading="Background",
                content=(
                    "Retrieval improves access "
                    "to external knowledge."
                ),
                citations=[citation],
            ),
            DraftSection(
                heading="Key Findings",
                content=(
                    "Retrieval improves access "
                    "to external knowledge."
                ),
                citations=[citation],
            ),
            DraftSection(
                heading="Discussion",
                content=(
                    "Retrieval improves access "
                    "to external knowledge."
                ),
                citations=[citation],
            ),
            DraftSection(
                heading="Conclusion",
                content=(
                    "Retrieval improves access "
                    "to external knowledge."
                ),
                citations=[citation],
            ),
        ]
    )
    result=evaluate_output(
        draft=draft,
        report=report,
        style_profile=None
    )

    assert result.grounding_score==1.0
    assert result.citation_correctness_score==1.0
    assert result.hallucination_safety_score==1.0
    assert result.format_compliance_score==1.0
    assert 0.0<=result.research_quality_score<=1.0
    assert 0.0<=result.overall_quality_score<=1.0