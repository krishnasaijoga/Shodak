from pydantic import BaseModel, Field

from shodak.llm.factory import get_llm
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.report import ResearchReport
from shodak.models.writing import WritingRequest
from shodak.style.profile import StyleProfile
from shodak.writing.templates import get_writing_template


class GeneratedSection(BaseModel):
    heading:str
    content:str


class GeneratedDraft(BaseModel):
    title:str
    sections:list[GeneratedSection]=Field(min_length=1)


def generate_draft_with_llm(
        report:ResearchReport,
        request:WritingRequest,
        style_profile:StyleProfile|None=None,
        style_examples:list[str]|None=None
)->WritingDraft:
    
    llm=get_llm().with_structured_output(GeneratedDraft)
    template=get_writing_template(request.output_type)
    
    evidence_text="\n".join(f"- {item.claim}" for item in report.evidence)

    contradiction_text="\n".join(
        (
            f"- {item.evidence_a.claim}\n"
            f" versus\n"
            f" {item.evidence_b.claim}"
        )
        for item in report.contradictions
    )

    style_profile_text=(
        style_profile.model_dump_json(indent=2)
        if style_profile is not None else "No Style profile available."
    )

    examples=style_examples or []
    style_examples_text="\n\n--\n\n".join(examples)

    prompt=f"""
You are the writing afent for Shodak.

Write a {request.output_type.value} based strictly on the supplied research.

Topic:
{report.request.topic}

Requested title:
{request.title or "Generate an appropriate title"}

Target word count:
{request.target_word_count}

Required structure:
{template}

Research evidence:
{evidence_text or "No evidence available."}

Conflicting evidence:
{contradiction_text or "No contradcitions identified."}

Writing style profile:
{style_profile_text}

Examples of the user's writing:
{style_examples_text or "No examples available."}

Requirements:
- Use only claims supported by the supplied evidence.
- Do not invent facts, studies, statistics, or citations.
- Preserve uncertainity where research is uncertain.
- Mention meaningful contradictions where relevant.
- Match the user's writing characteristics without copying the sentence.
- Follow the requested output structure.
- Stay reasonably close to the target word count.
- Return structured output only.
"""
    result=llm.invoke(prompt)
    return WritingDraft(
        output_type=request.output_type,
        title=result.title,
        sections=[
            DraftSection(
                heading=section.heading,
                content=section.content,
                citations=[]
            )
            for section in result.sections
        ]
    )