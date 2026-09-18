from shodak.models.source import PublicationStatus, Source, SourceProvider

PREPRINT_KEYWORDS={
    "arxiv",
    "biorxiv",
    "medrxiv",
    "ssrn",
    "research square",
}


def detect_publication_status(source:Source)->PublicationStatus:
    venue=(source.venue or "").lower()
    url=str(source.url).lower()
    if any(keyword in venue for keyword in PREPRINT_KEYWORDS):
        return PublicationStatus.preprint

    if any(keyword in url for keyword in PREPRINT_KEYWORDS):
        return PublicationStatus.preprint

    if source.provider==SourceProvider.crossref and source.doi:
        return PublicationStatus.peer_reviewed
    return PublicationStatus.unknown