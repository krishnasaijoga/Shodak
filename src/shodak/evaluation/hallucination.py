import re

from pydantic import BaseModel, Field

from shodak.models.draft import WritingDraft
from shodak.models.evidence import Evidence


class HallucinationResult(BaseModel):
    supported_sections:int
    unsupported_sections:int
    hallucination_risk:float=Field(ge=0.0,le=1.0)
    flagged_sections:list[str]


def _tokenize(text:str)->set[str]:
    return {
        word.lower() for word in re.findall(r"\b\w+\b",text) if len(word)>3
    }


def evaluate_hallucination(
        draft:WritingDraft,
        evidence_items:list[Evidence],
        minimum_overlap:int=2
)->HallucinationResult:
    supported_sections=0
    flagged_sections:list[str]=[]

    evidence_token_sets=[
        _tokenize(evidence.claim) for evidence in evidence_items
    ]

    for section in draft.sections:
        section_words=_tokenize(section.content)
        section_supported=any(
            len(section_words & evidence_words)>=minimum_overlap
            for evidence_words in evidence_token_sets
        )

        if section_supported:
            supported_sections+=1
        else:
            flagged_sections.append(section.heading)

    total_sections=len(draft.sections)
    unsupported_sections=total_sections-supported_sections

    hallucination_risk=(
        unsupported_sections/total_sections if total_sections else 0.0
    )

    return HallucinationResult(
        supported_sections=supported_sections,
        unsupported_sections=unsupported_sections,
        hallucination_risk=hallucination_risk,
        flagged_sections=flagged_sections
    )