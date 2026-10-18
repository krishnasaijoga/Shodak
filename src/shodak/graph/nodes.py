from shodak.evaluation.scorecard import evaluate_output
from shodak.graph.state import ShodakState
from shodak.observability import log_operation
from shodak.recovery import run_optional
from shodak.research.report import build_research_report
from shodak.research.synthesis import synthesize_research_with_fallback
from shodak.writing.generator import generate_draft
from shodak.writing.renderer import render_markdown
from shodak.writing.revision import revise_draft_with_llm


def research_node(state:ShodakState)->ShodakState:
    request=state["research_request"]
    try:
        with log_operation("research_node"):
            report=build_research_report(request)
        return {"research_report":report, "error":None}
    except Exception as exc:    # noqa: BLE001
        return {
            "error":str(exc)
        }



def writer_node(state:ShodakState)->ShodakState:
    with log_operation("writer_node"):
        report=state["research_report"]
        request=state["writing_request"]
        draft=generate_draft(
            report=report,
            request=request,
            style_profile=state.get("style_rpofile"),
            style_examples=state.get("style_examples",[]),
            research_synthesis=state.get("research_synthesis")
        )

    return {
        "writing_draft":draft
    }


def renderer_node(state:ShodakState)->ShodakState:
    with log_operation("renderer_node"):
        draft=state["writing_draft"]
        writing_request=state["writing_request"]
        rendered=render_markdown(
            draft,
            include_references=writing_request.include_references
        )

    return {
        "rendered_output":rendered
    }


def synthesis_node(state:ShodakState)->ShodakState:
    synthesis=run_optional(
        lambda: synthesize_research_with_fallback(state["research_report"]),
        operation_name="research_synthesis",
        fallback=None
    )
    return {
        "research_synthesis":synthesis
    }


def evaluator_node(
    state:ShodakState
)->ShodakState:
    try:
        with log_operation("evaluator_node"):
            draft=state["writing_draft"]
            report=state["research_report"]

            scorecard=evaluate_output(
                draft=draft,
                report=report,
                style_profile=state.get("style_profile")
            )

        return {
            "evaluation_scorecard":scorecard,
            "evaluation_error":None
        }
    except Exception as exc:    #noqa: BLE001
        return {
            "evaluation_scorecard":None,
            "evaluation_error":type(exc).__name__
        }


def revision_node(
    state:ShodakState
)->ShodakState:
    with log_operation("revision_node"):
        draft=state["writing_draft"]
        report=state["research_report"]
        scorecard=state["evaluation_scorecard"]
        revised_draft=revise_draft_with_llm(
            draft=draft,
            report=report,
            scorecard=scorecard
        )
    revision_count=state.get("revision_count",0)+1
    return {
        "writing_draft":revised_draft,
        "revision_count":revision_count
    }