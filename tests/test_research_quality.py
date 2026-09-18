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
    quality=evaluate_research_quality(sources=[source],evidence=[])
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
    quality=evaluate_research_quality(sources=sources,evidence=evidence)
    assert quality.sufficient_evidence is True
    assert quality.reason is None