from shodak.evaluation.format_compliance import evaluate_format_compliance
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.writing import OutputType


def test_blog_with_all_sections_is_compliance():
    draft=WritingDraft(
        output_type=OutputType.blog,
        title="Example Blog",
        sections=[
                    DraftSection(
                        heading="Introduction",
                        content="Intro",
                        citations=[]
                    ),
                    DraftSection(
                        heading="Key Findings",
                        content="Conclusion",
                        citations=[]
                    ),
                    DraftSection(
                        heading="Background",
                        content="Conclusion",
                        citations=[]
                    ),
                    DraftSection(
                        heading="Conclusion",
                        content="Conclusion",
                        citations=[]
                    ),
                    DraftSection(
                        heading="Discussion",
                        content="Conclusion",
                        citations=[]
                    )
                ]
    )
    result=evaluate_format_compliance(draft)
    assert result.compliance_score==1.0
    assert result.missing_sections==[]


def test_blog_with_missing_sections_has_lower_score():
    draft=WritingDraft(
        output_type=OutputType.blog,
        title="Example blog",
        sections=[
                    DraftSection(
                        heading="Introduction",
                        content="Intro",
                        citations=[]
                    ),
                    DraftSection(
                        heading="Conclusion",
                        content="Conclusion",
                        citations=[]
                    )
                ]
    )

    result=evaluate_format_compliance(draft)

    assert result.compliance_score<1.0
    assert "Background" in result.missing_sections
    assert "Key Findings" in result.missing_sections
    assert "Discussion" in result.missing_sections


def test_academic_structure_is_checked():
    draft=WritingDraft(
        output_type=OutputType.academic,
        title="Academic Draft",
        sections=[
            DraftSection(
                heading="Introduction",
                content="Intro",
                citations=[]
            ),
            DraftSection(
                heading="Evidence Review",
                content="Evidence",
                citations=[]
            ),
            DraftSection(
                heading="Critical Discussion",
                content="Limitations",
                citations=[]
            ),
            DraftSection(
                heading="Limitations",
                content="Limitations",
                citations=[]
            ),
            DraftSection(
                heading="Conclusion",
                content="Conclusion",
                citations=[],
            )
        ]
    )
    result=evaluate_format_compliance(draft)
    assert result.compliance_score==1.0


def test_linkedin_structure_is_checked():
    draft=WritingDraft(
        output_type=OutputType.linkedin,
        title="RAG",
        sections=[
            DraftSection(
                heading="Hook",
                content="Hook content",
                citations=[],
            ),
            DraftSection(
                heading="Context",
                content="Context",
                citations=[],
            ),
            DraftSection(
                heading="Key Insight",
                content="Insight",
                citations=[],
            ),
            DraftSection(
                heading="Evidence",
                content="Evidence",
                citations=[],
            ),
            DraftSection(
                heading="Takeaway",
                content="Takeaway",
                citations=[],
            )
        ]
    )
    result=evaluate_format_compliance(draft)
    assert result.compliance_score==1.0
    assert result.missing_sections==[]