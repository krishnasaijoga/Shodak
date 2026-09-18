from shodak.models.source import PublicationStatus, Source, SourceProvider, SourceType
from shodak.research.publication_status import detect_publication_status


def test_arxiv_source_is_preprint():
    source = Source(
        title="Example Preprint",
        url="https://arxiv.org/abs/1234.5678",
        source_type=SourceType.academic,
        provider=SourceProvider.semantic_scholar,
    )
    status=detect_publication_status(source)
    assert status==PublicationStatus.preprint


def test_unknown_source_remains_unknown():
    source = Source(
        title="Unknown Paper",
        url="https://example.com/paper",
        source_type=SourceType.academic,
        provider=SourceProvider.semantic_scholar,
    )
    status=detect_publication_status(source)
    assert status==PublicationStatus.unknown