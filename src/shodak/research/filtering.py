from shodak.models.source import Source

LOW_VALUE_TITLES={
    "front matter",
    "index",
    "list of authors",
    "table of contents",
    "contents",
    "acknowledgements",
    "acknowledgments",
    "preface"
}


def is_low_value_score(
        source:Source
)->bool:
    normalized_title=source.title.strip().lower()

    return normalized_title in LOW_VALUE_TITLES


def filter_low_value_sources(
        sources:list[Source]
)->list[Source]:
    return [
        source
        for source in sources
        if not is_low_value_score(source)
    ]