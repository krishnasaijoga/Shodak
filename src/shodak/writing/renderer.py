from shodak.models.draft import WritingDraft
from shodak.models.writing import OutputType
from shodak.writing.references import build_reference_list


def _render_linkedin(draft:WritingDraft)->str:
    lines:list[str]=[]
    for section in draft.sections:
        lines.append(section.content)
        lines.append("")
    return "\n".join(lines).strip()


def _render_structured_document(
        draft:WritingDraft,
        include_references:bool=True
)->str:
    lines:list[str]=[]
    lines.append(f"# {draft.title}")
    lines.append("")

    for section in draft.sections:
        lines.append(f"## {section.heading}")
        lines.append("")
        lines.append(section.content)
        lines.append("")

    if include_references:
        references=build_reference_list(draft)
        if references:
            lines.append("## References")
            lines.append("")
            for index, reference in enumerate(references,start=1):
                lines.append(f"{index}. {reference}")
            lines.append("")
    return "\n".join(lines)


def render_markdown(draft:WritingDraft, include_references:bool=True)->str:
    if draft.output_type==OutputType.linkedin:
        return _render_linkedin(draft)
    return _render_structured_document(draft,include_references=include_references)