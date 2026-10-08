from pydantic import BaseModel

from shodak.llm.router import invoke_structured_with_fallback
from shodak.models.contradiction import Contradiction
from shodak.models.evidence import Evidence


class ContradictionResult(BaseModel):
    is_contradiction:bool
    explanation:str


def detect_contradiction_with_llm(
    evidence_a:Evidence,
    evidence_b:Evidence
)->Contradiction | None:
    prompt=f"""
    You are comparing two research claims

    claim A:
    {evidence_a.claim}

    claim B:
    {evidence_b.claim}

    Determine whether the two claims meaningfully contradict each other.

    Requirements:
    - Do not mark them contradictory merely because they use different wording.
    - Distinguish contradiction from partial disagreement or different scope.
    - Return structured ouptut only.
    """
    result=invoke_structured_with_fallback(schema=ContradictionResult,prompt=prompt)
    if not result.is_contradiction:
        return None
    return Contradiction(
        topic="Semnatically conflicting evidence",
        evidence_a=evidence_a,
        evidence_b=evidence_b,
        explanation=result.explanation
    )


def detect_contradictions_with_llm(
    evidence_items:list[Evidence]
)->list[Contradiction]:
    contradictions:list[Contradiction]=[]

    for index, first in enumerate(evidence_items):
        for second in evidence_items[index+1:]:
            contradiction=detect_contradiction_with_llm(first, second)
            if contradiction is not None:
                contradictions.append(contradiction)
    return contradictions