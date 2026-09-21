from pydantic import BaseModel

from shodak.models.contradiction import Contradiction
from shodak.models.evidence import Evidence
from shodak.models.research import ResearchRequest
from shodak.models.source import Source


class ResearchQuality(BaseModel):
    sufficient_evidence:bool
    source_count:int
    evidence_count:int
    coverage_score:float=0.0
    reason:str|None=None



class ResearchReport(BaseModel):
    request: ResearchRequest
    research_questions:list[str]
    sources:list[Source]
    evidence:list[Evidence]
    contradictions:list[Contradiction]=[]
    quality:ResearchQuality