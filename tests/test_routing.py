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