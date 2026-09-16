import pytest
from pydantic import ValidationError

from shodak.models.research import ResearchDepth, ResearchRequest


def test_valid_research_request():
    request=ResearchRequest(topic="AI agents in healthcare")
    assert request.topic == "AI agents in healthcare"
    assert request.depth==ResearchDepth.standard
    assert request.max_sources==10



def test_invalid_short_topic():
    with pytest.raises(ValidationError):
        ResearchRequest(
            topic="AI agents in healthcare",
            max_sources=100
        )