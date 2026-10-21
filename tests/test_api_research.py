from unittest.mock import patch

from fastapi.testclient import TestClient

from shodak.api.app import app
from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport
from shodak.models.research import ResearchRequest

client = TestClient(app)


def test_research_endpoint():
    report = ResearchReport(
        request=ResearchRequest(topic="retrieval augmented generation"),
        research_questions=["What is retrieval augmented generation?"],
        sources=[],
        evidence=[
            Evidence(
                claim=("Retrieval improves access to external knowledge."),
                supporting_text="Supporting evidence.",
                citation=Citation(
                    source_title="RAG Paper",
                    source_url="https://example.com/rag",
                ),
                confidence=0.9,
            )
        ],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True, source_count=1, evidence_count=1, coverage_score=0.8
        ),
    )

    with patch("shodak.api.routes.research.build_research_report", return_value=report):
        response = client.post(
            "/research",
            json={
                "topic": "retrieval augmented generation",
                "depth": "standard",
                "max_sources": 10,
            },
        )
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "retrieval augmented generation"
    assert data["source_count"] == 0
    assert data["evidence_count"] == 1
    assert data["coverage_score"] == 0.8
    assert data["sufficient_evidence"] is True

    assert len(data["evidence"]) == 1
    assert data["evidence"][0]["source_title"] == "RAG Paper"
    assert data["evidence"][0]["confidence"] == 0.9


def test_research_endpoint_rejects_short_topic():
    response = client.post("/research", json={"topic": "AI"})
    assert response.status_code == 422
