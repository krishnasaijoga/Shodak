from shodak.models.source import Source
from shodak.research.doi import normalize_doi


def _normalize_title(title:str)->str:
    return " ".join(title.lower().split())


def deduplicate_sources(sources:list[Source])->list[Source]:
    seen_dois:set[str]=set()
    seen_titles:set[str]=set()
    unique_sources:list[Source]=[]

    for source in sources:
        doi=normalize_doi(source.doi)
        normalized_title=_normalize_title(source.title)
        if doi:
            if doi in seen_dois:
                continue
            seen_dois.add(doi)
        if normalized_title in seen_titles:
            continue
        seen_titles.add(normalized_title)
        unique_sources.append(source)
    return unique_sources