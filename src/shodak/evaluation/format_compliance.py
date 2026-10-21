from pydantic import BaseModel, Field

from shodak.models.draft import WritingDraft
from shodak.writing.templates import get_writing_template


class ForamtComplianceResult(BaseModel):
    required_sections: list[str]
    present_sections: list[str]
    missing_sections: list[str]
    compliance_score: float = Field(ge=0.0, le=1.0)


def evaluate_format_compliance(draft: WritingDraft) -> ForamtComplianceResult:
    required_sections = get_writing_template(draft.output_type)
    present_sections = [section.heading for section in draft.sections]
    normalized_present = {heading.strip().lower() for heading in present_sections}

    missing_sections = [
        heading
        for heading in required_sections
        if heading.strip().lower() not in normalized_present
    ]

    compliance_score = (
        (len(required_sections) - len(missing_sections)) / len(required_sections)
        if required_sections
        else 0.0
    )

    return ForamtComplianceResult(
        required_sections=required_sections,
        present_sections=present_sections,
        missing_sections=missing_sections,
        compliance_score=compliance_score,
    )
