from shodak.graph.state import ShodakState
from shodak.research.report import build_research_report


def research_node(state:ShodakState)->ShodakState:
    request=state["research_request"]
    report=build_research_report(request)
    return {"research_report":report}