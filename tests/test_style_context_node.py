from unittest.mock import patch

from shodak.graph.state import ShodakState
from shodak.graph.style_context import style_context_node
from shodak.models.writing import OutputType
from shodak.research.report import ResearchRequest
from shodak.style.profile import StyleDocument, StyleDocumentType
from shodak.writing.generator import WritingRequest


def test_style_node_adds_style_data():
    documents=[
        StyleDocument(
            title="Blog Example",
            document_type=StyleDocumentType.blog,
            content="I enjoy explaining AI systems through simple examples."
        )
    ]
    state:ShodakState={
        "research_request":ResearchRequest(
            topic="AI systems"
        ),
        "writing_request":WritingRequest(
            output_type=OutputType.blog
        )
    }
    with patch(
        "shodak.graph.style_context.load_style_corpus",
        return_value=documents
    ):
        result=style_context_node(state)
    assert result["style_document_type"]==StyleDocumentType.blog
    assert result["style_profile"] is not None
    assert isinstance(result["style_examples"],list)
