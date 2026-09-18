from shodak.models.source import PublicationStatus, Source, SourceProvider, SourceType
from shodak.research.credibility import credibililty_score
from shodak.research.normalizer import normalize_source


def test_peer_reviewed_source_scores_higher_than_unknown():
    peer_reviewed = normalize_source(
        Source(
            title="Peer Reviewed Paper",
            url="https://doi.org/10.1234/example",
            source_type=SourceType.academic,
            provider=SourceProvider.crossref,
            authors=["Krishna Joga"],
            publication_year=2026,
            abstract="A sufficiently detailed abstract for testing.",
            doi="10.1234/example",
            citation_count=100,
        )
    )

    unknown = normalize_source(
        Source(
            title="Unknown Academic Source",
            url="https://example.com/paper",
            source_type=SourceType.academic,
            provider=SourceProvider.semantic_scholar,
        )
    )
    assert peer_reviewed.publication_status==PublicationStatus.peer_reviewed
    assert credibililty_score(peer_reviewed)>credibililty_score(unknown)



def test_preprint_receives_lower_status_score():
    preprint = normalize_source(
        Source(
            title="Example Preprint",
            url="https://arxiv.org/abs/1234.5678",
            source_type=SourceType.academic,
            provider=SourceProvider.semantic_scholar,
        )
    )
    assert preprint.publication_status==PublicationStatus.preprint
    assert credibililty_score(preprint)>=1.0