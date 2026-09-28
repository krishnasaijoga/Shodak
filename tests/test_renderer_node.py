from unittest.mock import patch

from shodak.graph.nodes import renderer_node
from shodak.graph.state import ShodakState
from shodak.models.writing import OutputType, WritingRequest
from shodak.writing.generator import WritingDraft


def test_renderer_node_adds_rendered_output():
    writing_request=WritingRequest(
        output_type=OutputType.blog,
        include_references=True
    )
    draft=WritingDraft(
        output_type=OutputType.blog,
        title="AI agents in healthcare",
        sections=[]
    )
    state:ShodakState={
        "writing_request":writing_request,
        "writing_draft":draft
    }
    with patch(
        "shodak.graph.nodes.render_markdown",
        return_value="# AI agents in healthcare"
    ):
        result=renderer_node(state)
    assert  "rendered_ouptut" in result
    assert result["rendered_ouptut"]=="# AI agents in healthcare"