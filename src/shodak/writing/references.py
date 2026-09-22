from shodak.models.citation import Citation
from shodak.models.draft import WritingDraft


def collect_unique_citations(draft:WritingDraft)->list[Citation]:
    unique:list[Citation]=[]
    for section in draft.sections:
        for citation in section.citations:
            if citation not in unique:
                unique.append(citation)
    return unique


def format_reference(citation:Citation)->str:
    parts=[citation.source_title]
    if citation.publication_year is not None:
        parts.append(f"({citation.publication_year})")
    if citation.doi:
        parts.append(f"https://doi.org/{citation.doi}")
    else:
        parts.append(str(citation.source_url))
    return " ".join(parts)


def build_reference_list(draft:WritingDraft)->list[str]:
    citations=collect_unique_citations(draft)
    return [format_reference(citation) for citation in citations]