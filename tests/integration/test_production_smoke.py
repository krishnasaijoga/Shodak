from unittest.mock import MagicMock, patch

from shodak.graph.workflow import build_workflow
from shodak.models.research import ResearchRequest
from shodak.models.writing import OutputType, WritingRequest


def test_production_smoke():
    workflow=build_workflow()
    research_request=ResearchRequest(
        topic="retrieval augmented generation"
    )

    writing_request=WritingRequest(
        output_type=OutputType.blog
    )

    fake_report=MagicMock()
    fake_draft=MagicMock()
    fake_scorecard=MagicMock()

    with (
        patch("shodak.graph.nodes.build_research_report", return_value=fake_report),
        patch("shodak.graph.nodes.synthesize_research_with_fallback", return_value=None),
        patch("shodak.graph.nodes.generate_draft", return_value=fake_draft),
        patch("shodak.graph.nodes.evaluate_output",return_value=fake_scorecard),
        patch("shodak.graph.routing.should_revise",return_value=False),
        patch("shodak.graph.nodes.render_markdown",return_value="# Final Output")
    ):
        result=workflow.invoke(
            {
                "research_request":research_request,
                "writing_request":writing_request,
                "revision_count":0
            }
        )

    assert result["research_report"] is fake_report
    assert result["writing_draft"] is fake_draft
    assert result["rendered_output"] =="# Final Output"
    assert result["evaluation_scorecard"] is fake_scorecard


def test_production_smoke_optional_failure():
    workflow=build_workflow()

    research_request=ResearchRequest(
        topic="retrieval augmented generation"
    )

    writing_request=WritingRequest(
        output_type=OutputType.blog
    )

    fake_report=MagicMock()
    fake_draft=MagicMock()

    with (
        patch("shodak.graph.nodes.build_research_report",return_value=fake_report),
        patch("shodak.graph.nodes.synthesize_research_with_fallback",side_effect=RuntimeError("Synthesis unavailable")),
        patch("shodak.graph.nodes.generate_draft",return_value=fake_draft),
        patch("shodak.graph.nodes.evaluate_output",side_effect=RuntimeError("Evaluator unavailable")),
        patch("shodak.graph.nodes.render_markdown",return_value="# Recovered Ouptut")
    ):
        result=workflow.invoke(
            {
                "research_request":research_request,
                "writing_request":writing_request,
                "revision_count":0
            }
        )

    assert result["research_synthesis"] is None
    assert result["evaluation_scorecard"] is None
    assert result["rendered_output"]=="# Recovered Ouptut"


def test_writer_failure_remains_critical():
    workflow=build_workflow()
    research_request=ResearchRequest(
        topic="retrieval augmented generation"
    )

    writing_request=WritingRequest(
        output_type=OutputType.blog
    )

    with (
        patch("shodak.graph.nodes.build_research_report",return_value=None),
        patch("shodak.graph.nodes.synthesize_research_with_fallback",return_value=None),
        patch("shodak.graph.nodes.generate_draft",side_effect=RuntimeError("Writer failed"))
    ):
        try:
            workflow.invoke(
                {
                    "research_request":research_request,
                    "writing_request":writing_request,
                    "revision_count":0
                }
            )
        except RuntimeError:
            return

    raise AssertionError("Writer failure should remian critical.")