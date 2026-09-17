from enum import Enum

from pydantic import BaseModel, HttpUrl


class SourceType(str, Enum):
    academic="academic"
    official="official"
    technical="technical"
    community="community"
    general_web="general_web"


class SourceProvider(str,Enum):
    semantic_scholar="semantic_scholar"
    crossref="crossref"



class Source(BaseModel):
    title:str
    url:HttpUrl
    source_type:SourceType
    provider:SourceProvider
    authors:list[str]=[]
    publication_year:int|None=None
    abstract:str|None=None
    doi:str|None=None
    venue:str|None=None
    citation_count:int|None=None
    has_abstract:bool=False
    metadata_complete:bool=False