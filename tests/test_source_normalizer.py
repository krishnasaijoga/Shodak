from shodak.models.source import Source, SourceProvider, SourceType
from shodak.research.normalizer import normalize_source


def test_complete_source_is_marked_complete():
    source=Source(
        title="Example Paper",
        url="https://example.com/paper",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref,
        authors=["Joga Krishna"],
        publication_year=2025,
        abstract="Example abstract."
    )
    normalized=normalize_source(source)
    assert normalized.has_abstract is True
    assert normalized.metadata_complete is True


def test_incomplete_source_is_marked_incomplete():
    source=Source(
            title="Example Paper",
            url="https://example.com/paper",
            source_type=SourceType.academic,
            provider=SourceProvider.crossref
    )
    normalized=normalize_source(source)
    assert normalized.has_abstract is False
    assert normalized.metadata_complete is False