from unittest.mock import patch

from fastapi.testclient import TestClient

from shodak.api.app import app
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.writing import OutputType

client=TestClient(app)


def test_write_endpoint():
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
                citations=[],
            )
        ],
    )
    with patch(
        "shodak.api.routes.write.generate_draft",
        return_value=draft
    ):
        response=client.post(
            "/write",
            json={
                "topic": "retrieval augmented generation",
                "output_type": "blog",
                "target_word_count": 500,
                "evidence": [
                    {
                        "claim": (
                            "Retrieval improves access "
                            "to external knowledge."
                        ),
                        "supporting_text": (
                            "Supporting evidence."
                        ),
                        "source_title": "RAG Paper",
                        "source_url": (
                            "https://example.com/rag"
                        ),
                        "confidence": 0.9,
                    }
                ]
            }
        )

    assert response.status_code==200
    data=response.json()
    assert data["title"]=="Understanding RAG"
    assert "Retrieval improves access" in data["content"]
    assert data["evaluation"] is None


def test_write_endpoint_requires_evidence():
    response=client.post(
        "/write",
        json={
            "topic": "retrieval augmented generation",
            "output_type": "blog"
        }
    )

    assert response.status_code==422