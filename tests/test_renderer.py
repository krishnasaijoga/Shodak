from shodak.models.citation import Citation
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.writing import OutputType
from shodak.writing.renderer import render_markdown


def test_renderer_markdown():
    citation=Citation(
        source_title="Citation one",
        source_url="https://example.com/",
        publication_year=2025,
        doi="10.12345/example"
    )
    draft=WritingDraft(
        output_type=OutputType.linkedin,
        title="Example One",
        sections=[
            DraftSection(
                heading="Introduction",
                content="This is the introduction.",
                citations=[citation]
            ),
            DraftSection(
                heading="Conclusion",
                content="This is the conclusion",
                citations=[citation]
            )
        ]
    )
    rendered=render_markdown(draft)

    assert "# Example one".lower() in rendered.lower()
    assert "## Introduction".lower() in rendered.lower()
    assert "This is the introduction".lower() in rendered.lower()
    assert "## References".lower() in rendered.lower()
    assert "Citation One".lower() in rendered.lower()



def test_render_without_references():
    citation=Citation(
            source_title="Citation one",
            source_url="https://example.com/",
            publication_year=2025,
            doi="10.12345/example"
        )
    draft=WritingDraft(
        output_type=OutputType.linkedin,
        title="Example One",
        sections=[
            DraftSection(
                heading="Introduction",
                content="This is the introduction.",
                citations=[citation]
            ),
            DraftSection(
                heading="Conclusion",
                content="This is the conclusion",
                citations=[citation]
            )
        ]
    )

    rendered=render_markdown(draft,include_references=False)
    assert "# Example".lower() in rendered.lower()
    assert "## References".lower() not in rendered.lower()