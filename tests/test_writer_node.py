from unittest.mock import patch

from shodak.graph.nodes import writer_node
from shodak.graph.state import ShodakState
from shodak.models.research import ResearchRequest
from shodak.models.writing import OutputType, WritingRequest
from shodak.research.quality import ResearchQuality
from shodak.research.report import ResearchReport
from shodak.writing.generator import WritingDraft


def test_writer_node_adds_draft():
    research_request=ResearchRequest(
        topic="AI agents in healthcare"
    )

    writing_request=WritingRequest(
        output_type=OutputType.blog
    )

    report=ResearchReport(
        request=research_request,
        research_questions=[],
        sources=[],
        evidence=[],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=False,
            source_count=0,
            evidence_count=0,
            coverage_score=0.0,
            reason="Test Report"
        )
    )
    fake_draft=WritingDraft(
        output_type=OutputType.blog,
        title="AI agents in heathcare",
        sections=[]
    )
    state:ShodakState={
        "research_report":report,
        "writing_request":writing_request
    }
    with patch(
        "shodak.graph.nodes.generate_draft",
        return_value=fake_draft
    ):
        result=writer_node(state)
    assert "writing_draft" in result
    assert result["writing_draft"].title=="AI agents in heathcare"



def test_writer_node_passes_style_context():
    research_request=ResearchRequest(
        topic="AI agents in healthcare"
    )
    writing_request=WritingRequest(
        output_type=OutputType.blog
    )
    report=ResearchReport(
        request=research_request,
        research_questions=[],
        sources=[],
        evidence=[],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=False,
            source_count=0,
            evidence_count=0,
            coverage_score=0.0,
            reason="Test report."
        )
    )
    state:ShodakState={
        "research_report":report,
        "writing_request":writing_request,
        "style_profile":None,
        "style_examples":["Example passage written in my style."]
    }
    fake_draft=WritingDraft(
        output_type=OutputType.blog,
        title="AI agents in healthcare",
        sections=[]
    )
    with patch(
        "shodak.graph.nodes.generate_draft",
        return_value=fake_draft
    ) as mock_generate:
        result=writer_node(state)
    assert result["writing_draft"]==fake_draft

    mock_generate.assert_called_once_with(
        report=report,
        request=writing_request,
        style_profile=None,
        style_examples=["Example passage written in my style."],
        research_synthesis=None
    )