from unittest.mock import patch

from shodak.models.research import ResearchRequest
from shodak.models.source import Source, SourceProvider, SourceType
from shodak.research.normalizer import normalize_source
from shodak.research.report import build_research_report


def test_research_pipeline_end_to_end():
    source=normalize_source(
        Source(
            title="RAG Evaluation Paper",
            url="https://example.com/rag-paper",
            source_type=SourceType.academic,
            provider=SourceProvider.semantic_scholar,
            authors=["Joga Krishna", "Buddala Vyshu"],
            publication_year=2026,
            abstract=(
                "Retrieval augmented generation can improve access to external knowledge. "
                "Experiments show that retrieval quality can materially affect answer quality. "
                "Poor retrieval can still lead to unsupported model responses."
            ),
            doi="10.1234/example",
            citation_count=120,
        )
    )

    with patch("shodak.research.report.search_academic_sources",return_value=[source]):
        request=ResearchRequest(topic="retrieval augmented generation",max_sources=5)
        report=build_research_report(request)
    assert report.request.topic=="retrieval augmented generation"
    assert len(report.research_questions)>0
    assert len(report.sources)==1
    assert len(report.evidence)>0
    assert report.sources[0].metadata_complete is True
    assert report.sources[0].title=="RAG Evaluation Paper"
    first_evidence=report.evidence[0]
    assert first_evidence.citation.source_title=="RAG Evaluation Paper"
    assert first_evidence.citation.doi == "10.1234/example"
    assert first_evidence.confidence>0