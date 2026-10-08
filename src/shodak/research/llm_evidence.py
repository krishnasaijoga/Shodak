from pydantic import BaseModel, Field

from shodak.llm.router import invoke_structured_with_fallback
from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.models.source import Source


class ExtractedEvidenceItem(BaseModel):
    claim:str
    supporting_text:str
    confidence:float=Field(ge=0.0,le=1.0)


class ExtractedEvidence(BaseModel):
    items:list[ExtractedEvidenceItem]



def extract_evidence_with_llm(source:Source)->list[Evidence]:
    if not source.abstract:
        return []

    prompt=f"""
You are extracting evidence from an academic source.

Source title:
{source.title}

Abstract:
{source.abstract}

Extract only claims directly supported by the abstract.

Requirements:
- Do not invent instructions.
- Keep each claim concise.
- supporting_text must stay close to the source writing.
- confidence must represent how clarly the abstract supports the claim.
- Returns structured output only.
"""
    result=invoke_structured_with_fallback(schema=ExtractedEvidence, prompt=prompt)
    return [
        Evidence(
            claim=item.claim,
            supporting_text=item.supporting_text,
            citation=Citation(
                source_title=source.title,
                source_url=source.url,
                doi=source.doi,
                publication_year=source.publication_year
            )
        )
        for item in result.items
    ]