from pydantic import BaseModel, Field

from shodak.models.report import ResearchReport


class ResearchQualityEvaluation(BaseModel):
    source_score:float=Field(ge=0.0,le=1.0)
    evidence_score:float=Field(ge=0.0,le=1.0)
    coverage_score:float=Field(ge=0.0,le=1.0)
    contradiction_score:float=Field(ge=0.0,le=1.0)
    sufficiency_score:float=Field(ge=0.0,le=1.0)
    overall_research_quality:float=Field(ge=0.0,le=1.0)


def evaluate_research_quality(
    report:ResearchReport
)->ResearchQualityEvaluation:
    source_score=min(len(report.sources)/5,1.0)
    evidence_score=min(len(report.evidence)/5,1.0)
    coverage_score=report.quality.coverage_score
    contradiction_score=(
        1.0 if not report.contradictions else max(0.0,1.0-len(report.contradictions)*0.1)
    )

    sufficiency_score=(
        1.0 if report.quality.sufficient_evidence else 0.0
    )
    scores=[
        source_score,
        evidence_score,
        coverage_score,
        contradiction_score,
        sufficiency_score
    ]

    overall_research_quality=(
        sum(scores)/len(scores)
    )
    return ResearchQualityEvaluation(
        source_score=source_score,
        evidence_score=evidence_score,
        coverage_score=coverage_score,
        contradiction_score=contradiction_score,
        sufficiency_score=sufficiency_score,
        overall_research_quality=overall_research_quality
    )