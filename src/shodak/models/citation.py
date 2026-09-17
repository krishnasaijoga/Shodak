from pydantic import BaseModel, HttpUrl


class Citation(BaseModel):
    source_title:str
    source_url:HttpUrl
    doi:str|None=None
    publication_year:int|None=None