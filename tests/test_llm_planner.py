from unittest.mock import patch

from shodak.models.research import ResearchRequest
from shodak.research.llm_planner import ResearchPlan, build_llm_research_questions
from shodak.research.planner import build_research_questions_with_fallback


def test_llm_research_planner():
    request=ResearchRequest(
        topic="AI agents in healthcare"
    )
    fake_result=ResearchPlan(
            questions=[
                "What is retrieval augmented generation?",
                "How does retrieval improve model responses?",
                "What are the limitations of RAG?",
            ]
        )
    
    with patch(
        "shodak.research.llm_planner.invoke_structured_with_fallback",
        return_value=fake_result
    ):
        result=build_llm_research_questions(request)
    assert len(result)==3
    assert "retrieval" in result[0].lower()


def test_llm_planner_fals_back_to_deterministic():
    request=ResearchRequest(topic="AI agents in healthcare")
    with patch(
        "shodak.writing.llm_writer.invoke_structured_with_fallback",
        return_value=ResearchPlan(
            questions=[
                "What is retrieval augmented generation?",
                "How does retrieval improve model responses?",
                "What are the limitations of RAG?",
            ]
        )
    ):
        result=build_research_questions_with_fallback(request)
    assert len(result)>0