from shodak.models.contradiction import Contradiction
from shodak.models.evidence import Evidence

NEGATION_ITEMS=[
    "not",
    "no",
    "does not",
    "did not",
    "cannot",
    "fails to",
    "failed to"
]


def _contains_negation(text:str)->bool:
    normalized=text.lower()
    return any(term in normalized for term in NEGATION_ITEMS)


def detect_contradictions(
        evidence_items:list[Evidence]
)->list[Contradiction]:
    """Baseline, later replace with LLM model based semantic contradiction detection"""
    contradictions:list[Contradiction]=[]
    for index, first in enumerate(evidence_items):
        for second in evidence_items[index+1:]:
            first_negated=_contains_negation(first.claim)
            second_negated=_contains_negation(second.claim)

            if first_negated==second_negated:
                continue

            shared_words=set(first.claim.lower().split()) & set(second.claim.lower().split())

            if len(shared_words)<3:
                continue
            contradictions.append(Contradiction(
                topic="Potentially conflicting claim",
                evidence_a=first,
                evidence_b=second,
                explanation=("The claims share similar terminology but differ in their use of negation.")
            ))
    return contradictions