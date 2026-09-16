from shodak.models.research import ResearchDepth, ResearchRequest
from shodak.research.planner import build_research_questions


def test_standard_research_plan():
    request=ResearchRequest(topic="AI agents in healthcare")
    questions=build_research_questions(request)
    assert len(questions)==6
    assert "AI agents in healthcare" in questions[0]


def test_quick_research_plan():
    request=ResearchRequest(topic="AI agents in healthcare",depth=ResearchDepth.quick)
    questions=build_research_questions(request)
    assert len(questions)==3


def test_deep_research_plan():
    request=ResearchRequest(
        topic="AI agents in healthcare",
        depth=ResearchDepth.deep
    )
    questions=build_research_questions(request)
    assert len(questions)>=7