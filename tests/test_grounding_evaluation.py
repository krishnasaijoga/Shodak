from shodak.evaluation.grounding import evaluate_grounding
from shodak.models.citation import Citation
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.writing import OutputType


def test_grounding_score():
    citation=Citation(
        source_title="Example Paper",
        source_url="https://example.com/paper"
    )
    draft=WritingDraft(
        output_type=OutputType.blog,
        title="Example",
        sections=[
            DraftSection(
                heading="Introduction",
                content="Supported content.",
                citations=[citation]
            ),
            DraftSection(
                heading="Discussion",
                content="unsupported content.",
                citations=[]
            )
        ]
    )
    result=evaluate_grounding(
        draft=draft,
        evidence_items=[]
    )
    assert result.supported_sections==1
    assert result.total_sections==2
    assert result.grounding_scores==0.5
    assert result.unsupported_sections==["Discussion"]