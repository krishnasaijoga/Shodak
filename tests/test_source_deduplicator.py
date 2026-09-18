from shodak.models.source import Source, SourceProvider, SourceType
from shodak.research.deduplicator import deduplicate_sources


def test_duplciate_is_removed():
    first=Source(
        title="Example Paper",
        url="https://example.com/1",
        source_type=SourceType.academic,
        provider=SourceProvider.semantic_scholar,
        doi="10.1234/example"
    )
    second=Source(
        title="Example Paper from another Provider",
        url="https://example.com/2",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref,
        doi="10.1234/example"
    )

    result=deduplicate_sources([first,second])
    assert len(result)==1



def test_duplciate_title_is_removed():
    first = Source(
        title="Retrieval Augmented Generation",
        url="https://example.com/1",
        source_type=SourceType.academic,
        provider=SourceProvider.semantic_scholar
    )

    second = Source(
        title="  retrieval augmented generation  ",
        url="https://example.com/2",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref
    )
    result=deduplicate_sources([first,second])
    assert len(result)==1



def test_unique_sources_are_preserved():
    first = Source(
        title="Paper 1",
        url="https://example.com/1",
        source_type=SourceType.academic,
        provider=SourceProvider.semantic_scholar,
    )

    second = Source(
        title="Paper 2",
        url="https://example.com/2",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref,
    )
    result=deduplicate_sources([first,second])
    assert len(result)==2