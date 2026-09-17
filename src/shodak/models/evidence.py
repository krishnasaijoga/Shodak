from pydantic import BaseModel

from shodak.models.citation import Citation


class Evidence(BaseModel):
    claim:str
    supporting_text:str
    citation:Citation
    confidence:float