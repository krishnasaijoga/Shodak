from fastapi import APIRouter

from shodak.api.errors import LlmProviderUnavailableError, WorkflowExecutionError
from shodak.api.schemas import (
    EvaluationApiResponse,
    EvidenceApiResponse,
    ResearchApiResponse,
    RunApiRequest,
    RunApiResponse,
    WritingApiResponse,
)
from shodak.graph.workflow import build_workflow
from shodak.models.research import ResearchRequest
from shodak.models.writing import WritingRequest
from shodak.persistence import persist_completed_run

router=APIRouter(
    prefix="/run",
    tags=["workflow"]
)


@router.post(
    "",
    response_model=RunApiResponse
)
def run_shodak(request:RunApiRequest)->RunApiResponse:
    research_request=ResearchRequest(
        topic=request.topic,
        depth=request.depth,
        max_sources=request.max_sources
    )

    writing_request=WritingRequest(
        output_type=request.output_type,
        target_word_count=request.target_word_count
    )

    workflow=build_workflow()
    try:
        result=workflow.invoke(
            {
                "research_request":research_request,
                "writing_request":writing_request,
                "revision_count":0
            }
        )
        if result.get("error"):
            raise WorkflowExecutionError(message=result["error"])
    except RuntimeError as exc:
        message=str(exc)

        if "LLM provider" in message or "configured LLM providers" in message:
            raise LlmProviderUnavailableError() from exc
        raise WorkflowExecutionError() from exc

    report=result["research_report"]
    draft=result["writing_draft"]
    rendered_output=result["rendered_output"]
    scorecard=result["evaluation_scorecard"]

    evidence_response=[
        EvidenceApiResponse(
            claim=item.claim,
            source_title=item.citation.source_title,
            confidence=item.confidence
        )
        for item in report.evidence
    ]

    research_response=ResearchApiResponse(
        topic=report.request.topic,
        research_questions=report.research_questions,
        source_count=len(report.sources),
        evidence_count=len(report.evidence),
        coverage_score=report.quality.coverage_score,
        sufficient_evidence=report.quality.sufficient_evidence,
        evidence=evidence_response
    )

    evaluation_response=EvaluationApiResponse(
        grounding_score=scorecard.grounding_score,
        citation_correctness_score=scorecard.citation_correctness_score,
        hallucination_safety_score=scorecard.hallucination_safety_score,
        style_similarity_score=scorecard.style_similarity_score,
        format_compliance_score=scorecard.format_compliance_score,
        research_quality_score=scorecard.research_quality_score,
        overall_quality_score=scorecard.overall_quality_score
    )

    evaluation_data=(scorecard.model_dump(mode="json") if scorecard is not None else None)

    persist_completed_run(
        topic=request.topic,
        output_type=request.output_type.value,
        rendered_output=rendered_output,
        evaluation=evaluation_data
    )

    writing_response=WritingApiResponse(title=draft.title,content=rendered_output, evaluation=evaluation_response)
    return RunApiResponse(
        research=research_response,
        writing=writing_response
    )