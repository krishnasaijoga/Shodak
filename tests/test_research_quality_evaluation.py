from shodak.evaluation.research_quality import evaluate_research_quality
from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport
from shodak.models.research import ResearchRequest
from shodak.models.source import Source, SourceProvider, SourceType


def test_strong_research_has_high_quality_score():
    sources=[
        Source(
            title=f"Paper {index}",
            url=f"https://example.com/{index}",
            source_type=SourceType.academic,
            provider=SourceProvider.crossref
        )
        for index in range(5)
    ]
    evidence=[
        Evidence(
            claim=f"Evidence claim {index}",
            supporting_text="Supporting evidence.",
            citation=Citation(
                source_title=f"Paper {index}",
                source_url=f"https://example.com/{index}",
            ),
            confidence=0.9,
        )
        for index in range(5)
    ]

    report=ResearchReport(
        request=ResearchRequest(
            topic="retreival augmented generation"
        ),
        research_questions=[],
        sources=sources,
        evidence=evidence,
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=5,
            evidence_count=5,
            coverage_score=1.0
        )
    )
    result=evaluate_research_quality(report)
    assert result.source_score==1.0
    assert result.evidence_score==1.0
    assert result.coverage_score==1.0
    assert result.contradiction_score==1.0
    assert result.sufficiency_score==1.0
    assert result.overall_research_quality==1.0


def test_weak_research_has_lower_quality_score():
    report=ResearchReport(
        request=ResearchRequest(
            topic="retrieval augmented generation"
        ),
        research_questions=[],
        sources=[],
        evidence=[],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=False,
            source_count=0,
            evidence_count=0,
            coverage_score=0.2,
            reason="Insufficient evidence.",
        )
    )
    result=evaluate_research_quality(report)

    assert result.source_score==0.0
    assert result.evidence_score==0.0
    assert result.coverage_score==0.2
    assert result.sufficiency_score==0.0
    assert result.overall_research_quality<0.5