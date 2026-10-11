from pydantic import BaseModel, Field

from shodak.evaluation.scorecard import EvaluationScorecard
from shodak.llm.router import invoke_structured_with_fallback
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.report import ResearchReport
from shodak.writing.citation_grounding import find_relevant_citations


class RevisedSection(BaseModel):
    heading:str
    content:str


class RevisedDraft(BaseModel):
    title:str
    sections:list[RevisedSection]=Field(min_length=1)


def revise_draft_with_llm(
        draft:WritingDraft,
        report:ResearchReport,
        scorecard:EvaluationScorecard
)->WritingDraft:
    evidence_text="\n".join(
        f"- {evidence.claim}"
        for evidence in report.evidence
    )

    current_draft="\n\n".join(
        (
            f"{section.heading}\n"
            f"{section.content}"
        )
        for section in draft.sections
    )

    prompt=f"""
You are the revision agent for Shodak.

Revise the draft using the evaluation results and research evidence.

Current draft:
{current_draft}

Evaluation:
Grounding: {scorecard.grounding_score}
Citation correctness: {scorecard.citation_correctness_score}
Hallucination safety: {scorecard.hallucination_safety_score}
Style similarity: {scorecard.style_similarity_score}
Foramt Compliance: {scorecard.format_compliance_score}
Research quality: {scorecard.research_quality_score}
Overall quality: {scorecard.overall_quality_score}

Available research evidence:
{evidence_text}

Requirements:
- Remove or rewrite unsupported factual claim.
- Do not invent facts.
- Preserve claims that are supported by evidence.
- Imporove structure when format compliance is weak.
- Keep uncertainty where the evidence is uncertain.
- Preserve the original output type.
- Return structured output only.
"""

    result=invoke_structured_with_fallback(
        schema=RevisedDraft,
        prompt=prompt
    )
    return WritingDraft(
        output_type=draft.output_type,
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