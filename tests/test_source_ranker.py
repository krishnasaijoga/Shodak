from shodak.models.source import Source, SourceProvider, SourceType
from shodak.research.normalizer import normalize_source
from shodak.research.ranker import rank_sources, score_source


def test_source_with_more_evidence_scores_higher():
    strong=Source(
        title="Strong Paper",
        url="https://example.com/strong",
        source_type=SourceType.academic,
        provider=SourceProvider.semantic_scholar,
        authors=["Joga Krishna"],
        publication_year=2025,
        abstract="Detailed abstract."
    )
    weak=Source(
        title="Weak Paper",
        url="https://example.com/weak",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref
    )
    strong=normalize_source(strong)
    weak=normalize_source(weak)

    assert score_source(strong)>score_source(weak)



def test_rank_sources_orders_highest_first():
    high=Source(
        title="High",
            url="https://example.com/high",
            source_type=SourceType.academic,
            provider=SourceProvider.semantic_scholar,
            authors=["Jane Doe"],
            publication_year=2026,
        abstract="Abstract",
        citation_count=150
    )
    low=Source(
        title="Low",
        url="https://example.com/low",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref
    )

    high=normalize_source(high)
    low=normalize_source(low)
    ranked=rank_sources([low,high])
    assert ranked[0].title=="High"