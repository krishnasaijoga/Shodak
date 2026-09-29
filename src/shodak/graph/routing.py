from shodak.graph.state import ShodakState


def route_after_research(state:ShodakState)->str:
    if state.get("error"):
        return "error"
    return "writer"