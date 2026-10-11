from shodak.models.citation import Citation
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport
from shodak.models.research import ResearchRequest
from shodak.models.source import Source, SourceProvider, SourceType
from shodak.models.writing import OutputType


def build_good_report()->ResearchReport:
    citation=Citation(
        source_title="RAG Paper",
        source_url="https://example.com/rag"
    )
    evidence=[
        Evidence(
            claim="Retrieval improves access to external knowledge.",
            supporting_text="Supporting evidence.",
            citation=citation,
            confidence=0.9
        )
    ]
    sources=[
        Source(
            title="RAG Paper",
            url="https://example.com/rag",
            source_type=SourceType.academic,
            provider=SourceProvider.crossref
        )
    ]
    return ResearchReport(
        request=ResearchRequest(
            topic="retrieval augmented generation"
        ),
        research_questions=[],
        sources=sources,
        evidence=evidence,
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=1,
            evidence_count=1,
            coverage_score=0.9,
        )
    )


def build_good_blog()->WritingDraft:
    citation=Citation(
        source_title="RAG Paper",
        source_url="https://example.com/rag"
    )
    headings=[
        "Introduction",
        "Background",
        "Key Findings",
        "Discussion",
        "Conclusion"
    ]

    return WritingDraft(
        output_type=OutputType.blog,
        title="Understanding RAG",
        sections=[
            DraftSection(
                heading=heading,
                content=(
                    "Retrieval improves access "
                    "to external knowledge."
                ),
                citations=[citation],
            )
            for heading in headings
        ]
    )


def build_unsupported_blog()->WritingDraft:
    return WritingDraft(
        output_type=OutputType.blog,
        title="Unsupported RAG Claims",
        sections=[
            DraftSection(
                heading="Introduction",
                content=(
                    "RAG guarantees perfect accuracy "
                    "and reduces cost by ninety percent."
                ),
                citations=[],
            )
        ]
    )


def build_wrong_citation_blog()->WritingDraft:
    wrong_citation=Citation(
        source_title="Transformer Paper",
        source_url="https://example.com/transformer"
    )
    return WritingDraft(
        output_type=OutputType.blog,
        title="RAG",
        sections=[
            DraftSection(
                heading="Introduction",
                content=(
                    "Retrieval improves access "
                    "to external knowledge."
                ),
                citations=[wrong_citation],
            )
        ]
    )


def build_incomplete_blog()->WritingDraft:
    return WritingDraft(
        output_type=OutputType.blog,
        title="Incomplete Blog",
        sections=[
            DraftSection(
                heading="Introduction",
                content="Intro",
                citations=[],
            ),
            DraftSection(
                heading="Conclusion",
                content="Conclusion",
                citations=[],
            ),
        ]
    )