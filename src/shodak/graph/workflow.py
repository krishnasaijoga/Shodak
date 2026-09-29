from langgraph.graph import END, START, StateGraph

from shodak.graph.nodes import renderer_node, research_node, writer_node
from shodak.graph.routing import route_after_research
from shodak.graph.state import ShodakState


def build_workflow():
    graph=StateGraph(ShodakState)
    
    graph.add_node("research",research_node)
    graph.add_node("writer",writer_node)
    graph.add_node("renderer",renderer_node)

    graph.add_edge(START,"research")
    graph.add_conditional_edges(
        "research",
        route_after_research,
        {
            "writer": "writer"
        }
    )
    graph.add_edge("writer","renderer")
    graph.add_edge("renderer",END)

    return graph.compile()