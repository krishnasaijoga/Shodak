from shodak.models.evidence import Citation, Evidence
from shodak.models.source import Source


def extract_evidence_from_source(source:Source)->list[Evidence]:
    if not source.abstract:
        return []
    abstract=source.abstract.strip()
    if not abstract:
        return []
    sentences=[
        sentence.strip() for sentence in abstract.split(".") if sentence.strip()
    ]
    evidence_items=[]
    for sentence in sentences:
        if len(sentence)<40:
            continue
        evidence_items.append(
            Evidence(
                claim=sentence,
                supporting_text=sentence,
                citation=Citation(
                    source_title=source.title,
                    source_url=source.url,
                    doi=source.doi,
                    publication_year=source.publication_year
                ),
                confidence=0.6
            )
        )
    return evidence_items