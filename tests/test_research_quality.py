from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.models.source import Source, SourceProvider, SourceType
from shodak.research.quality import evaluate_research_quality


def test_insufficient_when_too_few_sources():
    source = Source(
        title="One Paper",
        url="https://example.com/1",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref,
    )
    quality = evaluate_research_quality(sources=[source], evidence=[])
    assert quality.sufficient_evidence is False


def test_sufficient_when_sources_and_evidence_are_present():
    sources = [
        Source(
            title="Paper One",
            url="https://example.com/1",
            source_type=SourceType.academic,
            provider=SourceProvider.crossref,
        ),
        Source(
            title="Paper Two",
            url="https://example.com/2",
            source_type=SourceType.academic,
            provider=SourceProvider.semantic_scholar,
        ),
    ]
    evidence = [
        Evidence(
            claim="Claim one with supporting evidence.",
            supporting_text="Evidence one.",
            citation=Citation(
                source_title="Paper One",
                source_url="https://example.com/1",
            ),
            confidence=0.6,
        ),
        Evidence(
            claim="Claim two with supporting evidence.",
            supporting_text="Evidence two.",
            citation=Citation(
                source_title="Paper Two",
                source_url="https://example.com/2",
            ),
            confidence=0.6,
        ),
    ]
    quality = evaluate_research_quality(sources=sources, evidence=evidence, coverage_score=0.5)
    assert quality.sufficient_evidence is True
    assert quality.reason is None


source_1 = Source(
    title="Paper One",
    url="https://example.com/paper-1",
    source_type=SourceType.academic,
    provider=SourceProvider.crossref,
)

source_2 = Source(
    title="Paper Two",
    url="https://example.com/paper-2",
    source_type=SourceType.academic,
    provider=SourceProvider.crossref,
)

evidence_1 = Evidence(
    claim="Support vector classifiers are commonly used for classification.",
    supporting_text="Evidence one.",
    citation=Citation(
        source_title="Paper One",
        source_url="https://example.com/1",
    ),
    confidence=0.8,
)

evidence_2 = Evidence(
    claim="Random forests provide another classical classification approach.",
    supporting_text="Evidence Two.",
    citation=Citation(
        source_title="Paper Two",
        source_url="https://example.com/2",
    ),
    confidence=0.8,
)


def test_research_quality_fails_when_coverage_is_low():
    quality = evaluate_research_quality(
        sources=[source_1, source_2], evidence=[evidence_1, evidence_2], coverage_score=0.0
    )
    assert quality.sufficient_evidence is False
    assert quality.coverage_score == 0.0


def test_research_quality_passes_with_sufficient_coverage():
    quality = evaluate_research_quality(
        sources=[source_1, source_2], evidence=[evidence_1, evidence_2], coverage_score=0.5
    )
    assert quality.sufficient_evidence is True
