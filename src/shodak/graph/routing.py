from shodak.evaluation.policy import should_revise
from shodak.graph.state import ShodakState

MAX_REVISIONS=2


def route_after_research(state:ShodakState)->str:
    if state.get("error"):
        return "error"
    return "writer"


def route_after_evaluation(
        state:ShodakState
)->str:
    scorecard=state["evaluation_scorecard"]
    revision_count=state.get("revision_count",0)
    if scorecard is None:
        return "render"
    if should_revise(scorecard) and revision_count<=MAX_REVISIONS:
        return "revise"
    return "render"