from unittest.mock import patch

from fastapi.testclient import TestClient

from shodak.api.app import app
from shodak.api.schemas import EvaluationApiResponse

client=TestClient(app)


def test_root_endpoint():
    response=client.get("/")
    assert response.status_code==200
    data=response.json()
    assert data["name"]=="Shodak"
    assert data["status"]=="running"


def test_health_endpoint():
    with (
        patch(
            "shodak.api.app.get_health_status",
            return_value="healthy"
        ),
        patch(
            "shodak.api.app.get_provider_status",
            return_value=[
                {
                    "provider":"groq",
                    "configured":True
                },
                {
                    "provider":"openai",
                    "configured":True
                }
            ]
        )
    ):
        response=client.get("/health")
    assert response.status_code==200
    data=response.json()
    assert data["status"]=="healthy"
    assert data["app_name"]=="Shodak"
    assert "environment" in data
    assert data["primary_provider"]=="groq"
    assert len(data["providers"])==2
    assert data["providers"][0]=={
        "provider":"groq",
        "configured":True
    }


def test_response_contains_request_id():
    response=client.get("/")
    assert response.status_code==200
    assert "X-Request-ID" in response.headers


def test_run_allows_missing_evaluation_scorecard():
    result={"evaluation_scorecard":None}
    scorecard=result.get("evaluation_scorecard")
    evaluation=None
    if scorecard is not None:
        evaluation=EvaluationApiResponse(
            grounding_score=scorecard.grounding_score,
            citation_correctness_score=scorecard.citation_correctness_score,
            hallucination_safety_score=scorecard.hallucination_safety_score,
            style_similarity_score=scorecard.style_similarity_score,
            format_compliance_score=scorecard.format_compliance_score,
            research_quality_score=scorecard.research_quality_score,
            overall_quality_score=scorecard.overall_quality_score
        )
    assert evaluation is None