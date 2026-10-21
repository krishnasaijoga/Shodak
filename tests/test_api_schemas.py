from shodak.api.schemas import (
    ResearchApiRequest,
    RunApiRequest,
    WriteApiRequest,
    WritingEvidenceInput,
)
from shodak.models.research import ResearchDepth
from shodak.models.writing import OutputType


def test_research_api_request_defaults():
    request = ResearchApiRequest(topic="retrieval augmented generation")
    assert request.depth == ResearchDepth.standard
    assert request.max_sources == 10


def test_write_api_request():
    request = WriteApiRequest(
        topic="retrieval augmented generation",
        output_type=OutputType.blog,
        evidence=[
            WritingEvidenceInput(
                claim="Retrieval improves access to external knowledge.",
                supporting_text="Supporting evidence.",
                source_title="RAG Paper",
                source_url="https://example.com/rag",
                confidence=0.9,
            )
        ],
    )
    assert request.output_type == OutputType.blog
    assert request.target_word_count == 800


def test_run_api_request():
    request = RunApiRequest(topic="retrieval augmented generation", output_type=OutputType.academic)
    assert request.depth == ResearchDepth.standard
    assert request.max_sources == 10
    assert request.target_word_count == 800
