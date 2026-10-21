from unittest.mock import patch

from shodak.graph.workflow import build_workflow
from shodak.models.research import ResearchRequest
from shodak.models.writing import OutputType, WritingRequest
from shodak.research.quality import ResearchQuality
from shodak.research.report import ResearchReport
from shodak.writing.generator import WritingDraft


def test_workflow_runs_end_to_end():
    research_request = ResearchRequest(topic="AI agents in healthcare")

    writing_request = WritingRequest(output_type=OutputType.blog)

    fake_report = ResearchReport(
        request=research_request,
        research_questions=[],
        sources=[],
        evidence=[],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=False,
            source_count=0,
            evidence_count=0,
            coverage_score=0.0,
            reason="Test report.",
        ),
    )

    fake_draft = WritingDraft(
        output_type=OutputType.blog, title="AI agents in healthcare", sections=[]
    )

    with (
        patch("shodak.graph.nodes.build_research_report", return_value=fake_report),
        patch("shodak.graph.nodes.generate_draft", return_value=fake_draft),
        patch("shodak.graph.nodes.render_markdown", return_value="# AI agents in healthcare"),
        patch("shodak.graph.routing.should_revise", return_value=False),
        patch(
            "shodak.graph.nodes.evaluate_output", side_effect=RuntimeError("Evaluator Failed")
        ) as mock_evaluate,
    ):
        workflow = build_workflow()
        result = workflow.invoke(
            {"research_request": research_request, "writing_request": writing_request}
        )

    assert "research_report" in result
    assert "writing_draft" in result
    assert "rendered_output" in result
    assert result["rendered_output"] == "# AI agents in healthcare"

    assert result["rendered_output"]
    assert result["evaluation_scorecard"] is None
    assert result["evaluation_error"] is None
    mock_evaluate.assert_not_called()
