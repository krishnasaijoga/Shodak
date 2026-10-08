import re

from shodak.models.citation import Citation
from shodak.models.evidence import Evidence


def _tokenize(text:str)->set[str]:
    return {
        word.lower() for word in re.findall(r"\b\w+\b",text) if len(word)>3
    }


def find_relevant_citations(
        text:str,
        evidence_items: list[Evidence],
        minimum_overlap:int =2
)->list[Citation]:
    text_words=_tokenize(text)
    citations:list[Citation]=[]
    for evidence in evidence_items:
        evidence_words=_tokenize(evidence.claim)
        overlap=text_words & evidence_words
        if len(overlap) < minimum_overlap:
            continue
        if evidence.citation not in citations:
            citations.append(evidence.citation)
    return citations