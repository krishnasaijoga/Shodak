from enum import Enum

from pydantic import BaseModel, Field


class ResearchDepth(str,Enum):
    quick="quick"
    standard="standard"
    deep="deep"


class ResearchRequest(BaseModel):
    topic: str = Field(min_length=3)
    depth: ResearchDepth = ResearchDepth.standard
    max_sources: int = Field(default=10,ge=1,le=50)
    include_academic: bool = True
    include_official: bool = True
    include_community: bool = True