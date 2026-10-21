import logging

from shodak.cache import build_cache_key, cache
from shodak.config import settings
from shodak.models.report import ResearchReport
from shodak.models.research import ResearchRequest
from shodak.research.academic import search_academic_sources
from shodak.research.contradictions import detect_contradictions_with_fallback
from shodak.research.coverage import calculate_research_coverage
from shodak.research.deduplicator import deduplicate_sources
from shodak.research.enrichment import enrich_sources
from shodak.research.evidence import extract_evidence
from shodak.research.evidence_deduplicator import deduplicate_evidence
from shodak.research.filtering import filter_low_value_sources
from shodak.research.planner import build_research_questions_with_fallback
from shodak.research.quality import evaluate_research_quality
from shodak.research.ranker import rank_sources

logger=logging.getLogger("shodak.cache")


def _build_research_report_uncached(request:ResearchRequest)->ResearchReport:
    questions=build_research_questions_with_fallback(request)
    sources=search_academic_sources(
        query=request.topic,
        limit=request.max_sources
    )

    unique_sources=deduplicate_sources(sources)

    filtered_sources=filter_low_value_sources(unique_sources)

    ranked_sources=rank_sources(filtered_sources)

    enriched_sources=enrich_sources(ranked_sources)

    evidence=[]

    for source in enriched_sources:
        evidence.extend(extract_evidence(source))
    evidence=deduplicate_evidence(evidence)

    coverage_score=calculate_research_coverage(questions,evidence)
    contradictions=detect_contradictions_with_fallback(evidence)
    quality=evaluate_research_quality(enriched_sources,evidence,coverage_score=coverage_score)
    return ResearchReport(
        request=request,
        research_questions=questions,
        sources=enriched_sources,
        evidence=evidence,
        contradictions=contradictions,
        quality=quality
    )


def build_research_report(
        request:ResearchRequest
)->ResearchReport:
    if not settings.cache_enabled:
        return _build_research_report_uncached(request)

    key=build_cache_key(
        namespace="research_report",
        payload=request.model_dump(mode="json")
    )

    cached=cache.get(key)

    if cached is not None:
        logger.info("cache_hit | namespace=research_report")
        return cached

    logger.info("cache_miss | namespace=research_report")

    report=_build_research_report_uncached(request)

    cache.set(
        key=key,
        value=report,
        ttl_seconds=settings.research_cache_ttl_seconds
    )
    
    return report