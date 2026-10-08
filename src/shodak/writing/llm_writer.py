from pydantic import BaseModel, Field

from shodak.llm.router import invoke_structured_with_fallback
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.report import ResearchReport
from shodak.models.synthesis import ResearchSynthesis
from shodak.models.writing import WritingRequest
from shodak.style.profile import StyleProfile
from shodak.writing.citation_grounding import find_relevant_citations
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
        style_examples:list[str]|None=None,
        research_synthesis:ResearchSynthesis|None=None
)->WritingDraft:
    
    template=get_writing_template(request.output_type)
    
    evidence_text="\n".join(f"- {item.claim}" for item in report.evidence)

    style_profile_text=(
        style_profile.model_dump_json(indent=2)
        if style_profile is not None else "No Style profile available."
    )

    examples=style_examples or []
    style_examples_text="\n\n--\n\n".join(examples)

    if research_synthesis is not None:
        findings_text="\n".join(
            (
                f"- {finding.finding}"
                f"(confidence: {finding.confidence})"
            )
            for finding in research_synthesis.key_findings
        )

        uncertainities_text="\n".join(
            f"- {item}" for item in research_synthesis.uncertainties
        )
        gaps_text="\n".join(
            f"- {item}" for item in research_synthesis.research_gaps
        )
        synthesis_contradictions_text="\n".join(
            f"- {item}" for item in research_synthesis.contradictions
        )
    else:
        findings_text="No research synthesis available."
        uncertainities_text="No synthesis uncertainties available."
        gaps_text="No research gaps identified."
        synthesis_contradictions_text="No synthesized contradiction available."

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

Synthesized key findings:
{findings_text}

Research uncertainties:
{uncertainities_text}

Research gaps:
{gaps_text}

Synthesized contradictions:
{synthesis_contradictions_text}

Raw supporting evidence:
{evidence_text or "No evidence available."}

Writing style profile:
{style_profile_text}

Examples of the user's writing:
{style_examples_text or "No examples available."}

Requirements:
- Use the synthesized findings as the main basis for the draft.
- Use raw evidence only to support or clarify those findings.
- Do not invent facts, studies, statistics, or citations.
- Preserve uncertainity where research is uncertain.
- Mention meaningful contradictions where relevant.
- Do not overstate weak findings.
- Match the user's writing characteristics without copying sentences.
- Follow the requested output structure.
- Stay reasonably close to the target word count.
- Return structured output only.
"""
    result=invoke_structured_with_fallback(schema=GeneratedDraft,prompt=prompt)
    return WritingDraft(
        output_type=request.output_type,
        title=result.title,
        sections=[
            DraftSection(
                heading=section.heading,
                content=section.content,
                citations=find_relevant_citations(
                    section.content,
                    report.evidence
                )
            )
            for section in result.sections
        ]
    )