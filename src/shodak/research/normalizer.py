from shodak.models.source import Source
from shodak.research.publication_status import detect_publication_status


def normalize_source(source:Source)->Source:
    source.has_abstract=bool(source.abstract)
    source.metadata_complete=all(
        [
            bool(source.title),
            bool(source.url),
            bool(source.authors),
            source.publication_year is not None
        ]
    )
    source.publication_status=detect_publication_status(source)
    return source