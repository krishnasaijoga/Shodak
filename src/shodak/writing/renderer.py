from shodak.models.draft import WritingDraft
from shodak.writing.references import build_reference_list


def render_markdown(
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