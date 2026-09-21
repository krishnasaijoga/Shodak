from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality
from shodak.models.source import Source


def evaluate_research_quality(
        sources:list[Source],
        evidence:list[Evidence],
        coverage_score:float=0.0
)->ResearchQuality:
    source_count=len(sources)
    evidence_count=len(evidence)
    if source_count<2:
        return ResearchQuality(
            sufficient_evidence=False,
            source_count=source_count,
            evidence_count=evidence_count,
            coverage_score=coverage_score,
            reason="Too few sources were found."
        )
    if evidence_count<2:
        return ResearchQuality(
            sufficient_evidence=False,
            source_count=source_count,
            evidence_count=evidence_count,
            coverage_score=coverage_score,
            reason="Too few supporting evidences were extracted."
        )
    return ResearchQuality(
        sufficient_evidence=True,
        source_count=source_count,
        coverage_score=coverage_score,
        evidence_count=evidence_count
    )