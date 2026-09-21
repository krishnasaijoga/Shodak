from pydantic import BaseModel

from shodak.models.evidence import Evidence


class Contradiction(BaseModel):
    topic:str
    evidence_a:Evidence
    evidence_b:Evidence
    explanation:str