from shodak.models.citation import Citation
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.report import ResearchReport
from shodak.models.writing import WritingRequest
from shodak.style.profile import StyleProfile
from shodak.writing.llm_writer import generate_draft_with_llm
from shodak.writing.templates import get_writing_template


def _build_evidence_summary(report:ResearchReport)->str:
    if not report.evidence:
        return "Insufficient evidence available to support this section"
    claims=[evidence.claim for evidence in report.evidence[:3]]
    return " ".join(claims)


def _collect_citations(report:ResearchReport)->list[Citation]:
    citations=[]
    for evidence in report.evidence[:3]:
        if evidence not in citations:
            citations.append(evidence.citation)
    return citations


def _build_contradiction_summary(report:ResearchReport)->str|None:
    if not report.contradictions:
        return None
    summaries=[]
    for contradiction in report.contradictions:
        summaries.append(
            f"{contradiction.evidence_a} \n\nHowever, another source reports: \n{contradiction.evidence_b}"
        )
    return " ".join(summaries)


def generate_draft_deterministic(
        report:ResearchReport,
        request:WritingRequest,
        style_profile:StyleProfile|None=None,
        style_examples:list[str]|None=None
)->WritingDraft:
    template=get_writing_template(request.output_type)
    title=request.title or report.request.topic.title()

    if not report.quality.sufficient_evidence:
        warning="The available research evidence is currently insufficient to produce a fully supported draft."
        return WritingDraft(
            output_type=request.output_type,
            title=title,
            sections=[
                DraftSection(
                    heading="Research Limitation",
                    content=warning,
                    citations=[]
                )
            ]
        )

    evidence_summary=_build_evidence_summary(report)
    citations=_collect_citations(report)
    contradiction_summary=_build_contradiction_summary(report)

    sections=[]
    for heading in template:
        sections.append(
            DraftSection(heading=heading,content=evidence_summary,citations=citations if request.include_citation else [])
        )

    if contradiction_summary:
        sections.append(
            DraftSection(
                heading="Conflicting Evidence",
                content=contradiction_summary,
                citations=citations if request.include_citation else []
            )
        )

    return WritingDraft(
        output_type=request.output_type,
        title=title,
        sections=sections
    )


def generate_draft(
        report:ResearchReport,
        request:WritingRequest,
        style_profile:StyleProfile|None=None,
        style_examples:list[str]|None=None
)->WritingDraft:
    if not report.quality.sufficient_evidence:
        return generate_draft_deterministic(
            report=report,
            request=request,
            style_profile=style_profile,
            style_examples=style_examples
        )
    try:
        return generate_draft_with_llm(
            report=report,
            request=request,
            style_profile=style_profile,
            style_examples=style_examples
        )
    except Exception: # noqa:BLE001
        return generate_draft_deterministic(
            report=report,
            request=request,
            style_profile=style_profile,
            style_examples=style_examples
        )