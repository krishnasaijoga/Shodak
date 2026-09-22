from pydantic import BaseModel

from shodak.models.citation import Citation
from shodak.models.writing import OutputType


class DraftSection(BaseModel):
    heading:str
    content:str
    citations:list[Citation]=[]



class WritingDraft(BaseModel):
    output_type:OutputType
    title:str
    sections:list[DraftSection]