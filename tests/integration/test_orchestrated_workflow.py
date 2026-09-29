from unittest.mock import patch

from shodak.graph.workflow import build_workflow
from shodak.models.writing import OutputType, WritingRequest
from shodak.research.quality import ResearchQuality
from shodak.research.report import ResearchReport, ResearchRequest
from shodak.writing.generator import WritingDraft


def test_orchestrated_workflow_success():
    research_request=ResearchRequest(
        topic="AI agents in healthcare"
    )
    writing_request=WritingRequest(
        output_type=OutputType.blog
    )
    fake_report=ResearchReport(
        request=research_request,
        research_questions=["What are AI agents?"],
        sources=[],
        evidence=[],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=2,
            evidence_count=2,
            coverage_score=0.5
        )
    )
    fake_draft=WritingDraft(
        output_type=OutputType.blog,
        title="AI agents in healthcare",
        sections=[]
    )
    workflow=build_workflow()
    with (
        patch(
            "shodak.graph.nodes.build_research_report",
            return_value=fake_report
        ),
        patch(
            "shodak.graph.nodes.generate_draft",
            return_value=fake_draft
        ),
        patch(
            "shodak.graph.nodes.render_markdown",
            return_value="# AI agents in healthcare"
        )
    ):
        result=workflow.invoke(
            {
                "research_request":research_request,
                "writing_request":writing_request
            }
        )
    assert result["research_report"] == fake_report
    assert result["writing_draft"] == fake_draft
    assert result["rendered_output"] == "# AI agents in healthcare"
    assert result["error"] is None



def test_orchestrated_workflow_failure():
    research_request=ResearchRequest(
        topic="AI agents in healthcare"
    )
    writing_request=WritingRequest(
        output_type=OutputType.blog
    )
    workflow=build_workflow()
    with patch(
        "shodak.graph.nodes.build_research_report",
        side_effect=RuntimeError("Research service unavailable")
    ):
        result=workflow.invoke(
            {
                "research_request":research_request,
                "writing_request":writing_request
            }
        )
    assert result["error"]=="Research service unavailable"
    assert "Shodak could not complete the request" in result["rendered_output"]
    assert "Research service unavailable" in result["rendered_output"]