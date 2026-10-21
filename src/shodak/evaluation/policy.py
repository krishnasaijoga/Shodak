from shodak.graph.state import ShodakState

MIN_OVERALL_QUALITY=0.75
MIN_GROUNDING=0.70
MIN_CITATION_CORRECTNESS=0.7
MIN_HALLUCINATION_SAFETY=0.8


def should_revise(
        state:ShodakState
)->str:
    report=state.get("research_report")
    if (report is not None and not report.quality.sufficient_evidence):
        return "render"

    scorecard=state.get("evaluation_scorecard")

    if scorecard is None:
        return "render"
    return "revise" if (
        scorecard.overall_quality_score<MIN_OVERALL_QUALITY
        or scorecard.grounding_score<MIN_GROUNDING
        or scorecard.citation_correctness_score<MIN_CITATION_CORRECTNESS
        or scorecard.hallucination_safety_score<MIN_HALLUCINATION_SAFETY
    ) else "render"