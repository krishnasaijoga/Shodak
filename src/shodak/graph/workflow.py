from langgraph.graph import END, START, StateGraph

from shodak.graph.errors import error_node
from shodak.graph.nodes import renderer_node, research_node, synthesis_node, writer_node
from shodak.graph.routing import route_after_research
from shodak.graph.state import ShodakState
from shodak.graph.style_context import style_context_node


def build_workflow():
    graph=StateGraph(ShodakState)
    
    graph.add_node("research",research_node)
    graph.add_node("writer",writer_node)
    graph.add_node("renderer",renderer_node)
    graph.add_node("error",error_node)
    graph.add_node("style_context",style_context_node)
    graph.add_node("synthesis",synthesis_node)

    graph.add_edge(START,"research")
    graph.add_conditional_edges(
        "research",
        route_after_research,
        {
            "writer": "synthesis",
            "error":"error"
        }
    )
    graph.add_edge("synthesis","style_context")
    graph.add_edge("style_context","writer")
    graph.add_edge("writer","renderer")
    graph.add_edge("renderer",END)
    graph.add_edge("error",END)

    return graph.compile()