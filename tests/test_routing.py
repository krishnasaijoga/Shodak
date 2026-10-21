from types import SimpleNamespace

from shodak.evaluation.policy import should_revise
from shodak.graph.nodes import evaluator_node
from shodak.graph.routing import route_after_evaluation, route_after_research
from shodak.graph.state import ShodakState
from shodak.research.quality import ResearchQuality
from shodak.research.report import ResearchReport, ResearchRequest


def test_route_after_research():
    report=ResearchReport(
        request=ResearchRequest(
            topic="AI agents"
        ),
        research_questions=[],
        sources=[],
        evidence=[],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=3,
            evidence_count=4,
            coverage_score=0.5
        )
    )
    state:ShodakState={
        "research_report":report
    }
    assert route_after_research(state)=="writer"


def test_missing_scorecard_routes_to_render():
    state={
        "evaluation_scorecard":None,
        "revision_count":0
    }
    result=route_after_evaluation(state)
    assert result=="render"


def test_insufficent_research_skips_revision():
    research_report = SimpleNamespace(
        quality=SimpleNamespace(
            sufficient_evidence=False
        )
    )

    state = {
        "research_report": research_report,
        "revision_count": 0,
        "evaluation_scorecard": SimpleNamespace(
            overall_quality_score=0.1
        ),
    }

    result = should_revise(state)

    assert result == "render"


def test_evaluator_skips_insufficent_research():
    state={
        "research_report":SimpleNamespace(
            quality=SimpleNamespace(sufficient_evidence=False)
        )
    }

    result=evaluator_node(state)

    assert result["evaluation_scorecard"] is None
    assert result["evaluation_error"] is None