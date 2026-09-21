from enum import Enum

from pydantic import BaseModel, Field


class OutputType(str,Enum):
    linkedin="Linkedin"
    blog="blog"
    academic="academic"
    thesis="thesis"



class WritingRequest(BaseModel):
    output_type:OutputType
    title:str|None=None
    target_word_count:int=Field(
        default=800,
        ge=100,
        le=10000
    )
    include_citation:bool=True
    include_references:bool=True