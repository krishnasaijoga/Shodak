from shodak.models.citation import Citation
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.report import ResearchReport
from shodak.models.synthesis import ResearchSynthesis
from shodak.models.writing import WritingRequest
from shodak.style.profile import StyleProfile
from shodak.writing.llm_writer import generate_draft_with_llm
from shodak.writing.postprocess import enforce_contradiction_handling
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


def _build_insufficient_evidence_content(
        heading:str,
        topic:str
):
    content_by_heading={
        "Introduction":f"This draft examines {topic}. However, the current research run did not retrieve enough reliable evidence to support a fully grounded discussion.",
        "Background":"The available source set is too limited to construct a reliable background synthesis.",
        "Key Findings":"No sufficiently supported findings were identified from the retrieved evidence.",
        "Discussion":"A meaningful discussion would require a broader and better-supported evidence base.",
        "Conclusion":"Further research is required before drawing strong conclusion on this topic.",
        "Evidence review":"The retrieved evidence is insifficient for a reliable evidence review.",
        "Critical Discussion":"Critical comparision is limited because the current research run produced too little usable evidence.",
        "Limitations":"The primary limitation is insufficient source coverage and supporting evidence.",
        "Literature Review":"The literature retrieved in this is insufficient for a substantive literature review.",
        "Evidence Synthesis":"A robust evidence synthesis cannot be produced from the current evidence set.",
        "Research Gap":"The immediate research gap is insuffcient retrieved and validated evidence on the topic.",
        "Hook":f"{topic} deserves careful analysis, but this research run did not retrieve evidence to support strong claims.",
        "Context":"The current evidence base is too limited for a fully grounded summary.",
        "Key Insight":"The strongest conclusion from this research run is that additional reliable evidence was retrieved.",
        "Takeaway":"A broader research pass is needed before making strong claims."
    }
    return content_by_heading.get(
                heading,
                "The available research evidence is currently insufficient to support this section."
            )

def generate_draft_deterministic(
        report:ResearchReport,
        request:WritingRequest,
        style_profile:StyleProfile|None=None,
        style_examples:list[str]|None=None
)->WritingDraft:
    template=get_writing_template(request.output_type)
    title=request.title or report.request.topic.title()

    if not report.quality.sufficient_evidence:
        sections=[
            DraftSection(
                heading=heading,
                content=_build_insufficient_evidence_content(
                    heading=heading,
                    topic=title
                ),
                citations=[]
            )
            for heading in template
        ]

        return WritingDraft(
            output_type=request.output_type,
            title=title,
            sections=sections
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
        style_examples:list[str]|None=None,
        research_synthesis:ResearchSynthesis|None=None
)->WritingDraft:
    if not report.quality.sufficient_evidence:
        draft=generate_draft_deterministic(
            report=report,
            request=request,
            style_profile=style_profile,
            style_examples=style_examples
        )
    else:
        try:
            draft=generate_draft_with_llm(
                report=report,
                request=request,
                style_profile=style_profile,
                style_examples=style_examples,
                research_synthesis=research_synthesis
            )
        except Exception: # noqa:BLE001
            draft=generate_draft_deterministic(
                report=report,
                request=request,
                style_profile=style_profile,
                style_examples=style_examples
            )
    return enforce_contradiction_handling(draft=draft, report=report)