from shodak.graph.state import ShodakState


def error_node(state:ShodakState)->ShodakState:
    error=state.get("error") or "An unknown workflow error occurred"
    return {
        "rendered_output":f"Shodak could not complete the request.\n\nReason: {error}"
    }