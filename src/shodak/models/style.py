from enum import Enum

from pydantic import BaseModel


class StyleDocumentType(str,Enum):
    blog="blog"
    research_paper="research_paper"
    linkedin="linkedin"
    other="other"


class StyleDocument(BaseModel):
    title:str
    document_type:StyleDocumentType
    content:str
    source_path:str|None=None