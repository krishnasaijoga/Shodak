from shodak.models.citation import Citation
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.writing import OutputType
from shodak.writing.references import build_reference_list, collect_unique_citations


def test_duplicate_citations_are_removed():
    citations=Citation(
        source_title="Citation One",
        source_url="https://example.com/"
    )
    draft=WritingDraft(
        output_type=OutputType.blog,
        title="Title One",
        sections=[
            DraftSection(
                heading="Introduction",
                content="Some content.",
                citations=[citations]
            ),
            DraftSection(
                heading="Conclusion",
                content="conclusion content",
                citations=[citations]
            )
        ]
    )
    result=collect_unique_citations(draft)
    assert len(result)==1



def test_reference_list_uses_doi_when_available():
    citations=Citation(
        source_title="Citation Two",
        source_url="https://example.com/",
        doi="10.1234/example",
        publication_year=2025
    )
    draft=WritingDraft(
        output_type=OutputType.academic,
        title="Title Two",
        sections=[
            DraftSection(
                heading="Introduction",
                content="More Content.",
                citations=[citations]
            )
        ]
    )
    references=build_reference_list(draft)
    assert len(references)==1
    assert "Citation Two" in references[0]
    assert "2025" in references[0]
    assert "https://doi.org/10.1234/example" in references[0]