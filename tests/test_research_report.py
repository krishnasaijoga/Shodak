from unittest.mock import patch

from shodak.models.research import ResearchRequest
from shodak.models.source import Source, SourceProvider, SourceType
from shodak.research.normalizer import normalize_source
from shodak.research.report import build_research_report


def test_build_research_report():
    source=normalize_source(
        Source(
            title="Example Paper",
            url="https://example.com/paper",
            source_type=SourceType.academic,
            provider=SourceProvider.semantic_scholar,
            authors=["Jane Doe"],
            publication_year=2025,
            abstract=(
                "Retrieval augmented generation can improve access to external knowledge. "
                "Research suggests that retrieval quality strongly affects answer quality."
            ),
            citation_count=25,
        )
    )
    with patch(
        "shodak.research.report.search_academic_sources",
        return_value=[source]
    ):
        request=ResearchRequest(
            topic="retrieval augmented generation",
            max_sources=5
        )
        report=build_research_report(request)
    assert report.request.topic=="retrieval augmented generation"
    assert len(report.research_questions)>0
    assert len(report.sources)==1
    assert len(report.evidence)>0