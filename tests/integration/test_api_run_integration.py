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

client=TestClient(app)

def test_run_api_integration():
    citation=Citation(
        source_title="RAG Paper",
        source_url="https://example.com/rag"
    )

    report=ResearchReport(
        request=ResearchRequest(
            topic="retrieval augmented generation"
        ),
        research_questions=["What is retrieval augmented generation?"],
        sources=[],
        evidence=[
            Evidence(
                claim=(
                        "Retrieval improves access "
                        "to external knowledge."
                    ),
                    supporting_text="Supporting evidence.",
                    citation=citation,
                    confidence=0.9
            )
        ],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=1,
            evidence_count=1,
            coverage_score=0.8
        )
    )
    draft=WritingDraft(
        output_type=OutputType.blog,
        title="Understanding RAG",
        sections=[
            DraftSection(
                heading="Introduction",
                content=(
                    "Retrieval improves access "
                    "to external knowledge."
                ),
                citations=[citation],
            )
        ]
    )

    scorecard=EvaluationScorecard(
        grounding_score=1.0,
        citation_correctness_score=1.0,
        hallucination_safety_score=1.0,
        style_similarity_score=0.9,
        format_compliance_score=1.0,
        research_quality_score=0.8,
        overall_quality_score=0.95
    )

    workflow=MagicMock()

    workflow.invoke.return_value={
        "research_report": report,
        "writing_draft": draft,
        "rendered_output": (
            "# Understanding RAG\n\n"
            "Retrieval improves access "
            "to external knowledge."
        ),
        "evaluation_scorecard": scorecard
    }

    with patch(
        "shodak.api.routes.run.build_workflow",
        return_value=workflow
    ):
        response=client.post(
            "/run",
            json={
                "topic": "retrieval augmented generation",
                "output_type": "blog",
                "depth": "standard",
                "max_sources": 10,
                "target_word_count": 500
            }
        )
    
    assert response.status_code==200
    data=response.json()

    assert data["research"]["evidence_count"]==1
    assert data["writing"]["title"]=="Understanding RAG"
    assert data["writing"]["evaluation"]["overall_quality_score"]==0.95

    workflow.invoke.assert_called_once()