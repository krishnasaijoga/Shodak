from shodak.models.report import ResearchReport
from shodak.models.research import ResearchRequest
from shodak.research.academic import search_academic_sources
from shodak.research.contradictions import detect_contradictions
from shodak.research.coverage import calculate_research_coverage
from shodak.research.deduplicator import deduplicate_sources
from shodak.research.evidence import extract_evidence_from_source
from shodak.research.evidence_deduplicator import deduplicate_evidence
from shodak.research.planner import build_research_questions
from shodak.research.quality import evaluate_research_quality
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
    evidence=deduplicate_evidence(evidence)
    coverage_score=calculate_research_coverage(questions,evidence)
    contradictions=detect_contradictions(evidence)
    quality=evaluate_research_quality(ranked_sources,evidence,coverage_score=coverage_score)
    return ResearchReport(
        request=request,
        research_questions=questions,
        sources=ranked_sources,
        evidence=evidence,
        contradictions=contradictions,
        quality=quality
    )