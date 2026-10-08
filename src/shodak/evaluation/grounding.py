from pydantic import BaseModel, Field

from shodak.models.draft import WritingDraft
from shodak.models.evidence import Evidence


class GroundingResult(BaseModel):
    supported_sections:int
    total_sections:int
    grounding_scores:float=Field(ge=0.0,le=1.0)
    unsupported_sections:list[str]


def evaluate_grounding(
    draft:WritingDraft,
    evidence_items:list[Evidence]
)->GroundingResult:
    supported_sections=0
    unsupported_sections:list[str]=[]

    for section in draft.sections:
        if section.citations:
            supported_sections+=1
        else:
            unsupported_sections.append(section.heading)
    total_sections=len(draft.sections)

    grounding_score=(
        supported_sections/total_sections if total_sections else 0.0
    )
    return GroundingResult(
        supported_sections=supported_sections,
        total_sections=total_sections,
        grounding_scores=grounding_score,
        unsupported_sections=unsupported_sections
    )