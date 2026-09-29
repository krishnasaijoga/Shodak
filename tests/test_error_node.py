from shodak.graph.errors import error_node
from shodak.graph.routing import route_after_research
from shodak.graph.state import ShodakState


def test_error_node_generates_output():
    state:ShodakState={
        "error":"Research provider failed"
    }
    result=error_node(state)
    assert "rendered_output" in result
    assert "Research provider failed" in result["rendered_output"]


def test_route_after_research_routes_errors():
    state:ShodakState={
        "error":"Something failed"
    }
    assert route_after_research(state)=="error"