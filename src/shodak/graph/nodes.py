from shodak.graph.state import ShodakState
from shodak.research.report import build_research_report
from shodak.writing.generator import generate_draft


def research_node(state:ShodakState)->ShodakState:
    request=state["research_request"]
    report=build_research_report(request)
    return {"research_report":report}



def writer_node(state:ShodakState)->ShodakState:
    report=state["research_report"]
    request=state["writing_request"]
    draft=generate_draft(
        report=report,
        request=request
    )
    return {
        "writing_draft":draft
    }