from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.report import ResearchReport
from shodak.models.writing import OutputType
from shodak.writing.citation_grounding import find_relevant_citations


def enforce_contradiction_handling(
        draft:WritingDraft,
        report:ResearchReport
)->WritingDraft:
    if not report.contradictions:
        return draft
    if draft.output_type==OutputType.linkedin:
        return draft
    existing_headings={
        section.heading.strip().lower() for section in draft.sections
    }

    if "conflicting evidence" in existing_headings:
        return draft

    contradiction_text="\n\n".join(
        (
            f"{item.evidence_a.claim} "
            f"However, {item.evidence_b.claim} "
            f"{item.explanation}"
        ) for item in report.contradictions
    )

    contradiction_section=DraftSection(
        heading="Conflicting Evidence",
        content=contradiction_text,
        citations=find_relevant_citations(
            contradiction_text,
            report.evidence
        )
    )
    sections=list(draft.sections)

    conclusion_index=next(
        (
            index
            for index, section in enumerate(sections)
            if section.heading.strip().lower()=="conclusion"
        ),
        len(sections)
    )

    sections.insert(conclusion_index,contradiction_section)

    return WritingDraft(
        output_type=draft.output_type,
        title=draft.title,
        sections=sections
    )