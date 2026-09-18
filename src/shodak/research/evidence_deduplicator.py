from shodak.models.evidence import Evidence


def _normalize_text(text:str)->str:
    return " ".join(text.lower().split())


def deduplicate_evidence(evidence_items:list[Evidence])->list[Evidence]:
    seen: set[str]=set()
    unique_items:list[Evidence]=[]
    for item in evidence_items:
        normalized_claim=_normalize_text(item.claim)
        if normalized_claim in seen:
            continue
        seen.add(normalized_claim)
        unique_items.append(item)
    return unique_items