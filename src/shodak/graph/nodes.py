from shodak.graph.state import ShodakState
from shodak.research.report import build_research_report
from shodak.writing.generator import generate_draft
from shodak.writing.renderer import render_markdown


def research_node(state:ShodakState)->ShodakState:
    request=state["research_request"]
    try:
        report=build_research_report(request)
        return {"research_report":report, "error":None}
    except Exception as exc:    # noqa: BLE001
        return {
            "error":str(exc)
        }



def writer_node(state:ShodakState)->ShodakState:
    report=state["research_report"]
    request=state["writing_request"]
    draft=generate_draft(
        report=report,
        request=request,
        style_profile=state.get("style_profile"),
        style_examples=state.get("style_examples",[])
    )

    return {
        "writing_draft":draft
    }


def renderer_node(state:ShodakState)->ShodakState:
    draft=state["writing_draft"]
    writing_request=state["writing_request"]
    rendered=render_markdown(
        draft,
        include_references=writing_request.include_references
    )

    return {
        "rendered_output":rendered
    }
