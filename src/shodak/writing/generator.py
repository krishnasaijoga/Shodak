from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.report import ResearchReport
from shodak.models.writing import WritingRequest
from shodak.writing.templates import get_writing_template


def build_evidence_summary(report:ResearchReport)->str:
    if not report.evidence:
        return "Insufficient evidence available to support this section"
    claims=[evidence.claim for evidence in report.evidence[:3]]
    return " ".join(claims)


def generate_draft(
        report:ResearchReport,
        request:WritingRequest
)->WritingDraft:
    template=get_writing_template(request.output_type)
    title=request.title or report.request.topic.title()
    evidence_summary=build_evidence_summary(report)

    sections=[]
    for heading in template:
        sections.append(
            DraftSection(heading=heading,content=evidence_summary)
        )

    return WritingDraft(
        output_type=request.output_type,
        title=title,
        sections=sections
    )