from unittest.mock import patch

from shodak.evaluation.scorecard import EvaluationScorecard
from shodak.graph.workflow import build_workflow
from shodak.models.writing import OutputType, WritingRequest
from shodak.research.quality import ResearchQuality
from shodak.research.report import ResearchReport, ResearchRequest
from shodak.writing.generator import WritingDraft


def test_orchestrated_workflow_success():
    research_request = ResearchRequest(topic="AI agents in healthcare")
    writing_request = WritingRequest(output_type=OutputType.blog)
    fake_report = ResearchReport(
        request=research_request,
        research_questions=["What are AI agents?"],
        sources=[],
        evidence=[],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True, source_count=2, evidence_count=2, coverage_score=0.5
        ),
    )
    fake_draft = WritingDraft(
        output_type=OutputType.blog, title="AI agents in healthcare", sections=[]
    )
    passing_scorecard = EvaluationScorecard(
        grounding_score=0.9,
        citation_correctness_score=0.9,
        hallucination_safety_score=0.9,
        style_similarity_score=0.9,
        format_compliance_score=1.0,
        research_quality_score=0.9,
        overall_quality_score=0.92,
    )

    with (
        patch("shodak.graph.nodes.build_research_report", return_value=fake_report),
        patch("shodak.graph.nodes.generate_draft", return_value=fake_draft),
        patch("shodak.graph.nodes.render_markdown", return_value="# AI agents in healthcare"),
        patch("shodak.graph.nodes.evaluate_output", return_value=passing_scorecard),
        patch("shodak.graph.routing.should_revise", return_value=False),
    ):
        workflow = build_workflow()
        result = workflow.invoke(
            {"research_request": research_request, "writing_request": writing_request}
        )
    assert result["research_report"] == fake_report
    assert result["writing_draft"] == fake_draft
    assert result["rendered_output"] == "# AI agents in healthcare"
    assert result["error"] is None


def test_orchestrated_workflow_failure():
    research_request = ResearchRequest(topic="AI agents in healthcare")
    writing_request = WritingRequest(output_type=OutputType.blog)
    workflow = build_workflow()
    with patch(
        "shodak.graph.nodes.build_research_report",
        side_effect=RuntimeError("Research service unavailable"),
    ):
        result = workflow.invoke(
            {"research_request": research_request, "writing_request": writing_request}
        )
    assert result["error"] == "Research service unavailable"
    assert "Shodak could not complete the request" in result["rendered_output"]
    assert "Research service unavailable" in result["rendered_output"]
