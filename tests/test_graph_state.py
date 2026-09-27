from shodak.graph.state import ShodakState
from shodak.models.research import ResearchRequest
from shodak.models.writing import OutputType, WritingRequest


def test_shodak_accepts_requests():
    state:ShodakState={
        "research_request":ResearchRequest(
            topic="AI Agents in healthcare"
        ),
        "writing_request":WritingRequest(
            output_type=OutputType.blog
        )
    }
    assert state["research_request"].topic=="AI Agents in healthcare"
    assert state["writing_request"].output_type==OutputType.blog