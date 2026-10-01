from unittest.mock import MagicMock, patch

from shodak.research.llm_planner import ResearchPlan, build_llm_research_questions
from shodak.research.planner import build_research_questions_with_fallback
from shodak.research.report import ResearchRequest


def test_llm_research_planner():
    request=ResearchRequest(
        topic="AI agents in healthcare"
    )
    structured_llm=MagicMock()
    structured_llm.invoke.return_value=ResearchPlan(
        questions=[
            "What are AI agents in healthcare",
            "What evidence supports their clinical use?",
            "What are their limitations and risks?"
        ]
    )
    base_llm=MagicMock()
    base_llm.with_structured_output.return_value=structured_llm

    with patch(
        "shodak.research.llm_planner.get_llm",
        return_value=base_llm
    ):
        result=build_llm_research_questions(request)
    assert len(result)==3
    assert "healthcare" in result[0].lower()


def test_llm_planner_fals_back_to_deterministic():
    request=ResearchRequest(topic="AI agents in healthcare")
    with patch(
        "shodak.research.planner.build_llm_research_questions",
        side_effect=RuntimeError("LLM unavailable")
    ):
        result=build_research_questions_with_fallback(request)
    assert len(result)>0