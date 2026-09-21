import json
from pathlib import Path
from unittest.mock import patch

from shodak.models.research import ResearchRequest
from shodak.models.source import Source, SourceProvider, SourceType
from shodak.research.normalizer import normalize_source
from shodak.research.report import build_research_report

BENCHMARK_FILE=(
    Path(__file__).resolve().parents[2]/"evaluation"/"research_benchmarks.json"
)


def test_research_quality_benchmarks():
    benchmarks=json.loads(BENCHMARK_FILE.read_text())
    mock_sources=[
        normalize_source(
            Source(
                title="Paper One",
                url="https://example.com/1",
                source_type=SourceType.academic,
                provider=SourceProvider.semantic_scholar,
                authors=["Krishna Joga"],
                publication_year=2025,
                abstract=("Retrieval augmented generation improves access to external knowledge. "
                    "Retrieval quality strongly affects answer quality."),
                citation_count=100
            )
        ),
        normalize_source(
            Source(
                title="Paper Two",
                url="https://example.com/2",
                source_type=SourceType.academic,
                provider=SourceProvider.crossref,
                authors=["Vyshnavi Buddala"],
                publication_year=2025,
                abstract=(
                    "Transformer attention mechanisms allow models to weigh contextual "
                    "relationships between tokens during representation learning."
                ),
                doi="10.1234/example",
                citation_count=50,
            )
        )
    ]
    with patch(
        "shodak.research.report.search_academic_sources",
        return_value=mock_sources
    ):
        for benchmark in benchmarks:
            report=build_research_report(
                ResearchRequest(
                    topic=benchmark["topic"],
                    max_sources=5
                )
            )
            assert len(report.sources)>=benchmark["expected_min_sources"]
            assert len(report.evidence)>=benchmark["expected_min_evidence"]
            assert (report.quality.coverage_score>=benchmark["expected_min_coverage"])