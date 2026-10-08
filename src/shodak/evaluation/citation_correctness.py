import re

from pydantic import BaseModel, Field

from shodak.models.draft import WritingDraft
from shodak.models.evidence import Evidence


class CitationCorrectnessResult(BaseModel):
    correct_citations:int
    total_citations:int
    citation_correctness_score:float=Field(ge=0.0,le=1.0)
    incorrect_sections:list[str]


def _tokenize(text:str)->set[str]:
    return {word.lower() for word in re.findall(r"\b\w+\b",text) if len(word)>3}


def evaluate_citation_correctness(
        draft:WritingDraft,
        evidence_item:list[Evidence],
        minimum_overlap:int=2
)->CitationCorrectnessResult:
    correct_citations=0
    total_citations=0
    incorrect_sections:list[str]=[]

    for section in draft.sections:
        section_words=_tokenize(section.content)
        section_has_incorrect_citation=False
        for citation in section.citations:
            total_citations+=1
            matching_evidence=[
                evidence for evidence in evidence_item if evidence.citation==citation
            ]

            citation_is_correct=False
            for evidence in matching_evidence:
                evidence_words=_tokenize(evidence.claim)
                overlap= section_words & evidence_words
                if len(overlap)>=minimum_overlap:
                    citation_is_correct=True
                    break
            if citation_is_correct:
                correct_citations+=1
            else:
                section_has_incorrect_citation=True
        if section_has_incorrect_citation:
            incorrect_sections.append(section.heading)
    citation_correctness_score=(correct_citations/total_citations if total_citations else 0.0)
    return CitationCorrectnessResult(
        correct_citations=correct_citations,
        total_citations=total_citations,
        citation_correctness_score=citation_correctness_score,
        incorrect_sections=incorrect_sections
    )