from pydantic import BaseModel, Field


class SynthesizedFinding(BaseModel):
    finding:str
    supporting_evidence_indices:list[int]
    confidence:float=Field(ge=0.0,le=1.0)


class ResearchSynthesis(BaseModel):
    key_findings:list[SynthesizedFinding]
    uncertainties:list[str]
    contradictions:list[str]
    research_gaps:list[str]
    overall_confidence:float=Field(ge=0.0,le=1.0)