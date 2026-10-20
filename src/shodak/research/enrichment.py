from shodak.models.source import Source
from shodak.research.academic import search_semantic_scholar
from shodak.research.exceptions import ResearchConnectionError, ResearchRateLimitError
from shodak.research.openalex import get_abstract_by_doi


def enrich_source(source:Source)->Source:
    if source.abstract:
        return source

    if not source.doi:
        return source

    try:
        results=search_semantic_scholar(
            query=source.doi,
            limit=1
        )

        if results:
            enriched=results[0]
            if enriched.abstract:
                return source.model_copy(
                    update={
                        "abstract":enriched.abstract,
                        "has_abstract":True
                    }
                )
    except (
        ResearchRateLimitError,
        ResearchConnectionError
    )as exc:
        print("SEMANTIC SCHOLAR ENRICHMENT FAILED: ",source.doi,type(exc).__name__)

    try:
        abstract=get_abstract_by_doi(source.doi)
    except (
                ResearchRateLimitError,
                ResearchConnectionError
            ) as exc:
                print("OPENALEX ENRICHMENT FAILED:", source.doi, type(exc).__name__)
                abstract=None
        
    if abstract:
        return source.model_copy(
            update={
                "abstract":abstract,
                "has_abstract":True
            }
        )

    return source


def enrich_sources(
        sources:list[Source]
)->list[Source]:
    return [
        enrich_source(source) for source in sources
    ]