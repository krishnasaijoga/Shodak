from unittest.mock import patch

from shodak.graph.nodes import research_node
from shodak.graph.state import ShodakState
from shodak.research.quality import ResearchQuality
from shodak.research.report import ResearchReport, ResearchRequest


def test_research_node_adds_report():
    request=ResearchRequest(
        topic="AI agents in healthcare"
    )
    fake_report=ResearchReport(
        request=request,
        research_questions=["What are AI agents"],
        sources=[],
        evidence=[],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=False,
            source_count=0,
            evidence_count=0,
            coverage_score=0.0,
            reason="Test report."
        )
    )
    state:ShodakState={
        "research_request":request
    }
    with patch(
        "shodak.graph.nodes.build_research_report",
        return_value=fake_report
    ):
        result=research_node(state)
        assert "research_report" in result
        assert result["research_report"].request.topic=="AI agents in healthcare"