from pydantic import BaseModel, HttpUrl


class Evidence(BaseModel):
    claim:str
    supporting_text:str
    source_title:str
    source_url:HttpUrl
    doi:str|None=None
    confidence:float