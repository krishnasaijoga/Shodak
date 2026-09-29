from shodak.graph.state import ShodakState


def route_after_research(state:ShodakState)->str:
    report=state["research_report"]
    if report.quality.sufficient_evidence:
        return "writer"
    return "writer"