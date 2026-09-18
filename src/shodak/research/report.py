from shodak.models.report import ResearchReport
from shodak.models.research import ResearchRequest
from shodak.research.academic import search_academic_sources
from shodak.research.deduplicator import deduplicate_sources
from shodak.research.evidence import extract_evidence_from_source
from shodak.research.planner import build_research_questions
from shodak.research.ranker import rank_sources


def build_research_report(request:ResearchRequest)->ResearchReport:
    questions=build_research_questions(request)
    sources=search_academic_sources(
        query=request.topic,
        limit=request.max_sources
    )
    unique_sources=deduplicate_sources(sources)
    ranked_sources=rank_sources(unique_sources)
    evidence=[]
    for source in ranked_sources:
        evidence.extend(extract_evidence_from_source(source))
    return ResearchReport(
        request=request,
        research_questions=questions,
        sources=ranked_sources,
        evidence=evidence
    )