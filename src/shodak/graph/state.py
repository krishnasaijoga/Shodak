from typing import TypedDict

from shodak.models.draft import WritingDraft
from shodak.models.report import ResearchReport
from shodak.models.research import ResearchRequest
from shodak.models.writing import WritingRequest


class ShodakState(TypedDict, total=False):
    research_request:ResearchRequest
    writing_request: WritingRequest
    research_report:ResearchReport
    writing_draft:WritingDraft
    rendered_ouptut:str
    error: str|None