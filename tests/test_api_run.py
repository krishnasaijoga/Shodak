from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from shodak.api.app import app
from shodak.evaluation.scorecard import EvaluationScorecard
from shodak.models.citation import Citation
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport
from shodak.models.research import ResearchRequest
from shodak.models.writing import OutputType

client = TestClient(app)


def test_run_endpoint():
    citation = Citation(source_title="RAG Paper", source_url="https://example.com/rag")

    report = ResearchReport(
        request=ResearchRequest(topic="retrieval augmented generation"),
        research_questions=["What is retrieval augmented generation?"],
        sources=[],
        evidence=[
            Evidence(
                claim=("Retrieval improves access to external knowledge."),
                supporting_text="Supporting evidence.",
                citation=citation,
                confidence=0.9,
            )
        ],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True, source_count=1, evidence_count=1, coverage_score=0.8
        ),
    )

    draft = WritingDraft(
        output_type=OutputType.blog,
        title="Understanding RAG",
        sections=[
            DraftSection(
                heading="Introduction",
                content=("Retrieval improves access to external knowledge."),
                citations=[citation],
            )
        ],
    )
    scorecard = EvaluationScorecard(
        grounding_score=1.0,
        citation_correctness_score=1.0,
        hallucination_safety_score=1.0,
        style_similarity_score=0.9,
        format_compliance_score=1.0,
        research_quality_score=0.8,
        overall_quality_score=0.95,
    )

    workflow = MagicMock()

    workflow.invoke.return_value = {
        "research_report": report,
        "writing_draft": draft,
        "rendered_output": (
            "# Understanding RAG\n\nRetrieval improves access to external knowledge."
        ),
        "evaluation_scorecard": scorecard,
    }

    with patch("shodak.api.routes.run.build_workflow", return_value=workflow):
        response = client.post(
            "/run",
            json={
                "topic": "retrieval augmented generation",
                "output_type": "blog",
                "depth": "standard",
                "max_sources": 10,
                "target_word_count": 500,
            },
        )

    assert response.status_code == 200

    data = response.json()
    assert data["research"]["topic"] == "retrieval augmented generation"

    assert data["research"]["evidence_count"] == 1

    assert data["writing"]["title"] == "Understanding RAG"

    assert "Retrieval improves access" in data["writing"]["content"]

    assert data["writing"]["evaluation"]["overall_quality_score"] == 0.95

    workflow.invoke.assert_called_once()


def test_run_endpoint_rejects_invalid_request():
    response = client.post("/run", json={"topic": "AI", "output_type": "blog"})
    assert response.status_code == 422


def test_run_endpoint_handles_provider_failure():
    workflow = MagicMock()

    workflow.invoke.side_effect = RuntimeError("All configured LLM providers failed.")

    with patch("shodak.api.routes.run.build_workflow", return_value=workflow):
        response = client.post(
            "/run", json={"topic": "retrieval augemented generation", "output_type": "blog"}
        )
    assert response.status_code == 503
    data = response.json()
    assert data["error"] == "llm_provider_unavailable"


def test_run_endpoint_handles_workflow_failure():
    workflow = MagicMock()

    workflow.invoke.side_effect = RuntimeError("Unexpected workflow failure.")

    with patch("shodak.api.routes.run.build_workflow", return_value=workflow):
        response = client.post(
            "/run", json={"topic": "retrieval augmented generation", "output_type": "blog"}
        )
    assert response.status_code == 500
    data = response.json()
    assert data["error"] == "workflow_execution_failed"


def test_run_endpoint_handles_graph_error_state():
    workflow = MagicMock()

    workflow.invoke.return_value = {"error": "Research service unavailable."}

    with patch("shodak.api.routes.run.build_workflow", return_value=workflow):
        response = client.post(
            "/run", json={"topic": "retrieval augmented generation", "output_type": "blog"}
        )
    assert response.status_code == 500
    data = response.json()
    assert data["error"] == "workflow_execution_failed"
    assert data["message"] == "Research service unavailable."


def test_run_rejects_excessively_long_topic():
    response = client.post(
        "/run",
        json={
            "topic": "a" * 501,
            "output_type": "blog",
            "depth": "standard",
            "max_sources": 10,
            "target_word_count": 800,
        },
    )

    assert response.status_code == 422


def test_run_rejects_excessive_word_count():
    response = client.post(
        "/run",
        json={
            "topic": "retrieval augmented generation",
            "output_type": "blog",
            "depth": "standard",
            "max_sources": 10,
            "target_word_count": 100_000,
        },
    )
    assert response.status_code == 422
