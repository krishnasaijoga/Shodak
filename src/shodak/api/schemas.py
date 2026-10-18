from pydantic import BaseModel, Field

from shodak.models.research import ResearchDepth
from shodak.models.writing import OutputType


class ResearchApiRequest(BaseModel):
    topic:str=Field(min_length=3,max_length=500)
    depth:ResearchDepth=ResearchDepth.standard
    max_sources:int=Field(default=10,ge=1,le=50)


class WritingEvidenceInput(BaseModel):
    claim:str=Field(min_length=1,max_length=5_000)
    supporting_text:str=Field(min_length=1,max_length=10_000)
    source_title:str=Field(min_length=1,max_length=500)
    source_url:str
    confidence:float=Field(ge=0.0,le=1.0)


class WriteApiRequest(BaseModel):
    topic:str=Field(min_length=3)
    output_type:OutputType
    target_word_count:int=Field(default=800, ge=100, le=10_000)
    evidence:list[WritingEvidenceInput]=Field(min_length=1)


class RunApiRequest(BaseModel):
    topic:str=Field(min_length=3,max_length=500)
    output_type:OutputType
    depth:ResearchDepth=ResearchDepth.standard
    max_sources:int=Field(default=10,ge=1,le=50)
    target_word_count:int=Field(default=800,ge=100,le=10_000)


class EvidenceApiResponse(BaseModel):
    claim:str
    source_title:str
    confidence:float


class ResearchApiResponse(BaseModel):
    topic:str
    research_questions:list[str]
    source_count:int
    evidence_count:int
    coverage_score:float
    sufficient_evidence:bool
    evidence:list[EvidenceApiResponse]


class EvaluationApiResponse(BaseModel):
    grounding_score:float
    citation_correctness_score: float
    hallucination_safety_score: float
    style_similarity_score: float
    format_compliance_score: float
    research_quality_score: float
    overall_quality_score: float


class WritingApiResponse(BaseModel):
    title:str
    content:str
    evaluation:EvaluationApiResponse | None= None


class RunApiResponse(BaseModel):
    research:ResearchApiResponse
    writing:WritingApiResponse


class ProviderStatus(BaseModel):
    provider:str
    configured:bool


class HealthApiResponse(BaseModel):
    status:str
    app_name:str
    environment:str
    primary_provider:str
    fallback_provider:str|None
    providers:list[ProviderStatus]
    startup_errors:list[str]=[]
    startup_warnings:list[str]=[]


class ErrorApiResponse(BaseModel):
    error:str
    message:str