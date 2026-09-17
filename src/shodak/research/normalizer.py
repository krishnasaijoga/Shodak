from shodak.models.source import Source


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
    return source