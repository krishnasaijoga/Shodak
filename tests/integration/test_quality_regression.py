from unittest.mock import patch

from shodak.evaluation.scorecard import EvaluationScorecard, evaluate_output
from shodak.graph.workflow import build_workflow
from shodak.models.citation import Citation
from shodak.models.draft import WritingDraft
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport
from shodak.models.research import ResearchRequest
from shodak.models.source import Source, SourceProvider, SourceType
from shodak.models.synthesis import ResearchSynthesis, SynthesizedFinding
from shodak.models.writing import OutputType, WritingRequest
from shodak.writing.llm_writer import GeneratedDraft, GeneratedSection
from tests.fixtures.quality_cases import build_good_report, build_unsupported_blog


def test_end_to_end_quality_regression():
    research_request=ResearchRequest(
        topic="retrieval augmented generation"
    )
    writing_request=WritingRequest(
        output_type=OutputType.blog,
        target_word_count=500
    )
    citation=Citation(
        source_title="RAG Paper",
        source_url="https://example.com/rag"
    )
    evidence=Evidence(
        claim=(
            "Retrieval improves access "
            "to external knowledge."
        ),
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
        request=research_request,
        research_questions=[
            "How does retrieval improve access to external knowledge?"
        ],
        sources=[source],
        evidence=[evidence],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=1,
            evidence_count=1,
            coverage_score=0.9,
        )
    )
    synthesis=ResearchSynthesis(
        key_findings=[
            SynthesizedFinding(
                finding=(
                    "Retrieval improves access to external knowledge."
                ),
                supporting_evidence_indices=[0],
                confidence=0.9
            )
        ],
        uncertainties=["Effectiveness depends on retrieval quality."],
        contradictions=[],
        research_gaps=[],
        overall_confidence=0.9
    )

    generated_draft=GeneratedDraft(
        title="Understanding Retrieval Augmented Generation",
        sections=[
            GeneratedSection(
                heading="Introduction",
                content=("Retrieval improves access to external knowledge.")
            ),
            GeneratedSection(
                heading="Background",
                content=("Retrieval improves access to external knowledge.")
            ),
            GeneratedSection(
                heading="Key Findings",
                content=(
                    "Retrieval improves access "
                    "to external knowledge."
                )
            ),
            GeneratedSection(
                heading="Discussion",
                content=(
                    "Retrieval improves access "
                    "to external knowledge."
                )
            ),
            GeneratedSection(
                heading="Conclusion",
                content=(
                    "Retrieval improves access "
                    "to external knowledge."
                )
            )
        ]
    )
    expected_scorecard=EvaluationScorecard(
        grounding_score=1.0,
        citation_correctness_score=1.0,
        hallucination_safety_score=1.0,
        format_compliance_score=1.0,
        style_similarity_score=1.0,
        research_quality_score=0.78,
        overall_quality_score=0.96
    )

    with (
        patch(
            "shodak.graph.nodes.build_research_report",
            return_value=report
        ),
        patch(
            "shodak.graph.nodes.synthesize_research_with_fallback",
            return_value=synthesis
        ),
        patch(
            "shodak.writing.llm_writer.invoke_structured_with_fallback",
            return_value=generated_draft
        ),
        patch(
            "shodak.graph.style_context.load_style_corpus",
            return_value=[]
        ),
        patch(
            "shodak.graph.routing.should_revise",
            return_value=False
        )
    ):
        workflow=build_workflow()
        result=workflow.invoke(
            {
                "research_request":research_request,
                "writing_request":writing_request
            }
        )

    assert result["research_report"]==report
    assert result["research_synthesis"]==synthesis
    assert isinstance(result["writing_draft"],WritingDraft)
    assert not result.get("error")

    scorecard=result["evaluation_scorecard"]

    assert scorecard.grounding_score>=expected_scorecard.grounding_score
    assert scorecard.citation_correctness_score>=expected_scorecard.citation_correctness_score
    assert scorecard.hallucination_safety_score>=expected_scorecard.hallucination_safety_score
    assert scorecard.format_compliance_score>=expected_scorecard.format_compliance_score
    assert scorecard.research_quality_score>=expected_scorecard.research_quality_score
    assert scorecard.overall_quality_score>=expected_scorecard.overall_quality_score

    draft=result["writing_draft"]

    assert all(
        section.citations for section in draft.sections
    )

    assert all(
        section.citations[0].source_title=="RAG Paper" for section in draft.sections
    )


def test_bad_output_fails_quality_threshold():
    result=evaluate_output(
        draft=build_unsupported_blog(),
        report=build_good_report(),
        style_profile=None
    )
    assert result.hallucination_safety_score<0.8
    assert result.overall_quality_score<0.8