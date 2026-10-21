from unittest.mock import patch

from shodak.models.source import Source, SourceProvider, SourceType
from shodak.research.enrichment import ResearchRateLimitError, enrich_source


def test_source_with_abstract_is_unchanged():
    source = Source(
        title="Test Paper",
        url="https://example.com/test",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref,
        abstract="Existing abstract",
        has_abstract=True,
    )

    result = enrich_source(source)

    assert result.abstract == "Existing abstract"


def test_source_is_enriched_by_doi():
    source = Source(
        title="Test Paper",
        url="https://doi.org/10.1234/test",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref,
        doi="10.1234/test",
        abstract=None,
        has_abstract=False,
    )

    enriched_result = Source(
        title="Test Paper",
        url="https://example.com/test",
        source_type=SourceType.academic,
        provider=SourceProvider.semantic_scholar,
        doi="10.1234/test",
        abstract="Useful abstract",
        has_abstract=True,
    )

    with patch(
        "shodak.research.enrichment.search_semantic_scholar", return_value=[enriched_result]
    ):
        result = enrich_source(source)

    assert result.abstract == "Useful abstract"

    assert result.has_abstract is True


def test_source_remains_unchanged_when_no_enrichment_found():
    source = Source(
        title="Test Paper",
        url="https://doi.org/10.1234/test",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref,
        doi="10.1234/test",
        abstract=None,
        has_abstract=False,
    )

    with patch("shodak.research.enrichment.search_semantic_scholar", return_value=[]):
        result = enrich_source(source)

    assert result.abstract is None
    assert result.has_abstract is False


def test_openalex_used_when_semantic_scholar_fails():
    source = Source(
        title="Test Paper",
        url="https://doi.org/10.1234/test",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref,
        doi="10.1234/test",
        abstract=None,
        has_abstract=False,
    )

    with (
        patch(
            "shodak.research.enrichment.search_semantic_scholar",
            side_effect=ResearchRateLimitError("Rate limited"),
        ),
        patch("shodak.research.enrichment.get_abstract_by_doi", return_value="OpenAlex abstract."),
    ):
        result = enrich_source(source)

    assert result.abstract == "OpenAlex abstract."
    assert result.has_abstract is True
