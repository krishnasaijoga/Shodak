from fastapi import APIRouter

from shodak.api.schemas import WriteApiRequest, WritingApiResponse
from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport
from shodak.models.research import ResearchRequest
from shodak.models.writing import WritingRequest
from shodak.writing.generator import generate_draft
from shodak.writing.renderer import render_markdown

router=APIRouter(
    prefix="/write",
    tags=["writing"]
)


@router.post(
    "",
    response_model=WritingApiResponse
)
def write(
    request:WriteApiRequest
)->WritingApiResponse:
    evidence=[
        Evidence(
            claim=item.claim,
            supporting_text=item.supporting_text,
            citation=Citation(
                source_title=item.source_title,
                source_url=item.source_url
            ),
            confidence=item.confidence
        )
        for item in request.evidence
    ]

    research_report=ResearchReport(
        request=ResearchRequest(
            topic=request.topic,
        ),
        research_questions=[],
        sources=[],
        evidence=evidence,
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=len(evidence),
            evidence_count=len(evidence),
            coverage_score=1.0,
        )
    )

    writing_request=WritingRequest(
        output_type=request.output_type,
        target_word_count=request.target_word_count
    )

    draft=generate_draft(
        report=research_report,
        request=writing_request
    )

    content=render_markdown(
        draft=draft,
        include_references=True
    )

    return WritingApiResponse(
        title=draft.title,
        content=content,
        evaluation=None
    )