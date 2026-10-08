from shodak.llm.factory import get_llm
from shodak.models.report import ResearchReport
from shodak.models.synthesis import ResearchSynthesis
from shodak.research.synthesis_fallback import synthesize_research_deterministic


def synthesize_research(
        report:ResearchReport
)->ResearchSynthesis:
    llm=get_llm().with_structured_output(ResearchSynthesis)

    evidence_text="\n".join(
        (
            f"[{index}] {evidence.claim}\n"
            f"Source: {evidence.citation.source_title}\n"
            f"Confidence: {evidence.confidence}"
        )
        for index,evidence in enumerate(report.evidence)
    )

    contradiction_text="\n".join(
        (
            f"- {item.evidence_a.claim}\n"
            f" vs\n"
            f" {item.evidence_b.claim}\n"
            f" Explanation: {item.explanation}"
        )
        for item in report.contradictions
    )
    prompt=f"""
You are te research synthesis component of Shodak.

Topic:
{report.request.topic}

Research evidence:
{evidence_text or "No evidence available."}

Known contradictions:
{contradiction_text or "No contradiction identified."}

Research coverage score:
{report.quality.coverage_score}

Tasks:
- Synthesize the strongest findings supported by the supplied evidence.
- Do not introduce information not present in the evidence.
- Group related evidence into broader findings where appropriate.
- Record the evidence indices that support each finding.
- Clearly identify uncertainity.
- Preserve meaningful contradictions.
- Identify research gaps when the available evidence does not fully answer the topic.
- Assign confidence based only on the supplied evidence.
- Return structured output only.
"""
    return llm.invoke(prompt)


def synthesize_research_with_fallback(
        report:ResearchReport
)->ResearchSynthesis:
    try:
        return synthesize_research(report)
    except Exception: # noqa BLE001
        return synthesize_research_deterministic(report)