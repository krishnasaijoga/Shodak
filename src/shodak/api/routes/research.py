from fastapi import APIRouter

from shodak.api.errors import LlmProviderUnavailableError, WorkflowExecutionError
from shodak.api.schemas import EvidenceApiResponse, ResearchApiResponse
from shodak.models.research import ResearchRequest
from shodak.research.report import build_research_report

router=APIRouter(
    prefix="/research",
    tags=["research"]
)

@router.post(
    "",
    response_model=ResearchApiResponse
)
def research(
    request:ResearchRequest
)->ResearchApiResponse:
    research_request=ResearchRequest(
        topic=request.topic,
        depth=request.depth,
        max_sources=request.max_sources
    )
    try:
        report=build_research_report(
            research_request
        )
    except RuntimeError as exc:
        message=str(exc)
        if "LLM provider" in message or "configured LLM providers" in message:
            raise LlmProviderUnavailableError() from exc
        raise WorkflowExecutionError(message="Research could not be completed.") from exc

    evidence=[
        EvidenceApiResponse(
            claim=item.claim,
            source_title=item.citation.source_title,
            confidence=item.confidence
        )
        for item in report.evidence
    ]

    return ResearchApiResponse(
        topic=report.request.topic,
        research_questions=report.research_questions,
        source_count=len(report.sources),
        evidence_count=len(report.evidence),
        coverage_score=report.quality.coverage_score,
        sufficient_evidence=report.quality.sufficient_evidence,
        evidence=evidence
    )