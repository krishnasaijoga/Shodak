from pydantic import BaseModel, Field

from shodak.evaluation.citation_correctness import evaluate_citation_correctness
from shodak.evaluation.format_compliance import evaluate_format_compliance
from shodak.evaluation.grounding import evaluate_grounding
from shodak.evaluation.hallucination import evaluate_hallucination
from shodak.evaluation.research_quality import evaluate_research_quality
from shodak.evaluation.style_similarity import evaluate_style_similarity
from shodak.models.draft import WritingDraft
from shodak.models.report import ResearchReport
from shodak.style.profile import StyleProfile


class EvaluationScorecard(BaseModel):
    grounding_score:float=Field(ge=0.0,le=1.0)
    citation_correctness_score:float=Field(ge=0.0,le=1.0)
    hallucination_safety_score:float=Field(ge=0.0,le=1.0)
    style_similarity_score:float=Field(ge=0.0,le=1.0)
    format_compliance_score:float=Field(ge=0.0,le=1.0)
    research_quality_score:float=Field(ge=0.0,le=1.0)
    overall_quality_score:float=Field(ge=0.0,le=1.0)



def evaluate_output(
        draft:WritingDraft,
        report:ResearchReport,
        style_profile:StyleProfile|None=None
)->EvaluationScorecard:
    grounding=evaluate_grounding(
        draft=draft,evidence_items=report.evidence
    )
    citation_correctness=evaluate_citation_correctness(
        draft=draft,evidence_items=report.evidence
    )
    hallucination=evaluate_hallucination(
        draft=draft,evidence_items=report.evidence
    )
    format_compliance=evaluate_format_compliance(draft=draft)
    research_quality=evaluate_research_quality(report=report)

    if style_profile is not None:
        style_similarity_score=evaluate_style_similarity(draft=draft,target_profile=style_profile).overall_style_similarity
    else:
        style_similarity_score=1.0
    hallucination_safety_score=(1.0-hallucination.hallucination_risk)
    scores=[
        grounding.grounding_score,
        citation_correctness.citation_correctness_score,
        hallucination_safety_score,
        style_similarity_score,
        format_compliance.compliance_score,
        research_quality.overall_research_quality
    ]
    overall_quality_score=sum(scores)/len(scores)

    return EvaluationScorecard(
        grounding_score=grounding.grounding_score,
        citation_correctness_score=citation_correctness.citation_correctness_score,
        hallucination_safety_score=hallucination_safety_score,
        style_similarity_score=style_similarity_score,
        format_compliance_score=format_compliance.compliance_score,
        research_quality_score=research_quality.overall_research_quality,
        overall_quality_score=overall_quality_score
    )