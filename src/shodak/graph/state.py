from typing import TypedDict

from shodak.models.draft import WritingDraft
from shodak.models.report import ResearchReport
from shodak.models.research import ResearchRequest
from shodak.models.style import StyleDocumentType
from shodak.models.synthesis import ResearchSynthesis
from shodak.models.writing import WritingRequest
from shodak.style.profile import StyleProfile


class ShodakState(TypedDict, total=False):
    research_request:ResearchRequest
    writing_request: WritingRequest
    research_report:ResearchReport
    writing_draft:WritingDraft
    rendered_output:str
    error: str|None
    style_document_type:StyleDocumentType
    style_profile:StyleProfile|None
    style_examples:list[str]
    research_synthesis:ResearchSynthesis