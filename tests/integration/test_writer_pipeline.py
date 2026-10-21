from unittest.mock import patch

from shodak.models.citation import Citation
from shodak.models.contradiction import Contradiction
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport, ResearchRequest
from shodak.models.writing import OutputType, WritingRequest
from shodak.writing.generator import generate_draft
from shodak.writing.llm_writer import GeneratedDraft, GeneratedSection
from shodak.writing.renderer import render_markdown


def test_writer_pipeline_end_to_end():
    evidence_a = Evidence(
        claim="Retrieval improves access to external knowledge.",
        supporting_text="Supporting evidence A.",
        citation=Citation(
            source_title="Paper One",
            source_url="https://example.com/1",
            doi="10.1234/one",
            publication_year=2025,
        ),
        confidence=0.8,
    )
    evidence_b = Evidence(
        claim="Retrieval does not always improve answer quality.",
        supporting_text="Supporting evidence B.",
        citation=Citation(
            source_title="Paper Two",
            source_url="https://example.com/2",
            doi="10.1234/two",
            publication_year=2026,
        ),
        confidence=0.8,
    )
    report = ResearchReport(
        request=ResearchRequest(topic="retrieval augmented generation"),
        research_questions=[
            "What is retrieval augmented generation?",
            "What are its benefits and limitations?",
        ],
        sources=[],
        evidence=[evidence_a, evidence_b],
        contradictions=[
            Contradiction(
                topic="Retrieval effectiveness",
                evidence_a=evidence_a,
                evidence_b=evidence_b,
                explanation="The sources report different outcomes.",
            )
        ],
        quality=ResearchQuality(
            sufficient_evidence=True, source_count=2, evidence_count=2, coverage_score=0.5
        ),
    )
    writing_request = WritingRequest(
        output_type=OutputType.blog,
        title="Understanding Retrieval Augmented Generation",
        include_citation=True,
        include_references=True,
    )

    with patch(
        "shodak.writing.llm_writer.invoke_structured_with_fallback",
        return_value=GeneratedDraft(
            title="Understanding Retrieval Augmented Generation",
            sections=[
                GeneratedSection(
                    heading="Introduction",
                    content="Retrieval augmented generation uses external knowledge.",
                ),
                GeneratedSection(
                    heading="Background",
                    content="Retrieval can provide additional context.",
                ),
                GeneratedSection(
                    heading="Key Findings",
                    content="Retrieval may improve access to external knowledge.",
                ),
                GeneratedSection(
                    heading="Discussion",
                    content="Its effectiveness varies across cases.",
                ),
                GeneratedSection(
                    heading="Conflicting Evidence",
                    content=(
                        "The available evidence reports different outcomes "
                        "for retrieval effectiveness."
                    ),
                ),
                GeneratedSection(
                    heading="Conclusion",
                    content="The evidence suggests benefits with limitations.",
                ),
            ],
        ),
    ):
        draft = generate_draft(report, writing_request)

    rendered = render_markdown(draft, include_references=writing_request.include_references)
    assert draft.title.lower() == "Understanding Retrieval Augmented Generation".lower()
    headings = [section.heading for section in draft.sections]
    assert "Introduction" in headings
    assert "Conflicting Evidence" in headings
    assert "## References" in rendered
    assert "Paper One" in rendered
    assert "Paper Two" in rendered
