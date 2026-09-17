from pydantic import BaseModel

from shodak.models.evidence import Evidence
from shodak.models.research import ResearchRequest
from shodak.models.source import Source


class ResearchReport(BaseModel):
    request: ResearchRequest
    research_questions:list[str]
    sources:list[Source]
    evidence:list[Evidence]