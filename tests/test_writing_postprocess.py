from shodak.models.citation import Citation
from shodak.models.contradiction import Contradiction
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport
from shodak.models.research import ResearchRequest
from shodak.models.writing import OutputType
from shodak.writing.postprocess import enforce_contradiction_handling


def test_contradictions_are_always_surfaced():
    evidence_a=Evidence(
        claim="Retrieval improves access to external knowledge.",
        supporting_text="Supporting evidence A.",
        citation=Citation(
            source_title="Paper One",
            source_url="https://example.com/1",
        ),
        confidence=0.8
    )
    evidence_b=Evidence(
        claim="Retrieval does not always improve answer quality.",
        supporting_text="Supporting evidence B.",
        citation=Citation(
            source_title="Paper Two",
            source_url="https://example.com/2",
        ),
        confidence=0.8
    )
    report=ResearchReport(
        request=ResearchRequest(
            topic="retrieval augmented generation"
        ),
        research_questions=[],
        sources=[],
        evidence=[
            evidence_a,
            evidence_b,
        ],
        contradictions=[
            Contradiction(
                topic="Retrieval effectiveness",
                evidence_a=evidence_a,
                evidence_b=evidence_b,
                explanation=(
                    "The sources report different outcomes."
                ),
            )
        ],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=2,
            evidence_count=2,
            coverage_score=0.8,
        )
    )

    draft=WritingDraft(
        output_type=OutputType.blog,
        title="Understanding RAG",
        sections=[
            DraftSection(
                heading="Introduction",
                content="Introduction content.",
                citations=[],
            ),
            DraftSection(
                heading="Discussion",
                content="Discussion content.",
                citations=[],
            ),
            DraftSection(
                heading="Conclusion",
                content="Conclusion content.",
                citations=[],
            ),
        ]
    )
    result=enforce_contradiction_handling(
        draft=draft,
        report=report
    )
    headings=[
        section.heading for section in result.sections
    ]

    assert "Conflicting Evidence" in headings

    conflicting_index=headings.index("Conflicting Evidence")

    conclusion_index=headings.index("Conclusion")

    assert conflicting_index<conclusion_index



def test_existing_conflicting_evidence_section_is_not_duplicated():
    evidence_a = Evidence(
        claim="Retrieval improves access to external knowledge.",
        supporting_text="Supporting evidence A.",
        citation=Citation(
            source_title="Paper One",
            source_url="https://example.com/1",
        ),
        confidence=0.8,
    )

    evidence_b = Evidence(
        claim="Retrieval does not always improve answer quality.",
        supporting_text="Supporting evidence B.",
        citation=Citation(
            source_title="Paper Two",
            source_url="https://example.com/2",
        ),
        confidence=0.8,
    )

    report = ResearchReport(
        request=ResearchRequest(
            topic="retrieval augmented generation"
        ),
        research_questions=[],
        sources=[],
        evidence=[
            evidence_a,
            evidence_b,
        ],
        contradictions=[
            Contradiction(
                topic="Retrieval effectiveness",
                evidence_a=evidence_a,
                evidence_b=evidence_b,
                explanation=(
                    "The sources report different outcomes."
                ),
            )
        ],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=2,
            evidence_count=2,
            coverage_score=0.8,
        ),
    )

    draft = WritingDraft(
        output_type=OutputType.blog,
        title="Understanding RAG",
        sections=[
            DraftSection(
                heading="Introduction",
                content="Introduction content.",
                citations=[],
            ),
            DraftSection(
                heading="Conflicting Evidence",
                content=(
                    "The available evidence reports "
                    "different outcomes."
                ),
                citations=[],
            ),
            DraftSection(
                heading="Conclusion",
                content="Conclusion content.",
                citations=[],
            ),
        ],
    )

    result = enforce_contradiction_handling(
        draft=draft,
        report=report,
    )

    conflicting_sections = [
        section
        for section in result.sections
        if section.heading.strip().lower()
        == "conflicting evidence"
    ]

    assert len(conflicting_sections) == 1


def test_no_contradictions_does_not_add_section():
    report = ResearchReport(
        request=ResearchRequest(
            topic="retrieval augmented generation"
        ),
        research_questions=[],
        sources=[],
        evidence=[],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=0,
            evidence_count=0,
            coverage_score=0.8,
        ),
    )

    draft = WritingDraft(
        output_type=OutputType.blog,
        title="Understanding RAG",
        sections=[
            DraftSection(
                heading="Introduction",
                content="Introduction content.",
                citations=[],
            ),
            DraftSection(
                heading="Conclusion",
                content="Conclusion content.",
                citations=[],
            ),
        ],
    )

    result = enforce_contradiction_handling(
        draft=draft,
        report=report,
    )

    headings = [
        section.heading
        for section in result.sections
    ]

    assert "Conflicting Evidence" not in headings