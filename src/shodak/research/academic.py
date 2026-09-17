import httpx

from shodak.models.source import Source, SourceType
from shodak.research.exceptions import (
    ResearchConnectionError,
    ResearchProviderError,
    ResearchRateLimitError,
)

SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
CROSSREF_URL = "https://api.crossref.org/works"


def search_semantic_scholar(query:str, limit:int=5)->list[Source]:
    params={
        "query":query,
        "limit":limit,
        "fields":"title,url,authors,year,abstract,venue,citationCount,externalIds"
    }

    try:
        response=httpx.get(
            SEMANTIC_SCHOLAR_URL, params=params,timeout=20.0
        )
        if response.status_code==429:
            raise ResearchRateLimitError("Semantic Scholar Rate limit reached.")
        response.raise_for_status()
    except httpx.TimeoutException as exc:
        raise ResearchConnectionError("Semantic Scholar request timed out.") from exc

    payload=response.json()

    sources=[]
    for paper in payload.get("data",[]):
        external_ids=paper.get("externalIds") or {}
        url=paper.get("url")
        if not url:
            continue
        source=Source(
            title=paper["title"],
            url=paper.get("url"),
            source_type=SourceType.academic,
            authors=[
                author["name"] for author in paper.get("authors",[]) if author.get("name")
            ],
            publication_year=paper.get("year"),
            abstract=paper.get("abstract"),
            doi=external_ids.get("DOI"),
            venue=paper.get("venue"),
            citation_count=paper.get("citationCount")
        )
        sources.append(source)
    return sources



def search_crossref(query:str,limit:int=5)->list[Source]:
    params={
        "query.bibliographic":query,
        "rows":limit
    }

    try:
        response=httpx.get(CROSSREF_URL,params=params,timeout=20.0)

        if response.status_code==429:
            raise ResearchRateLimitError("Crossref limit rate reached.")
        response.raise_for_status()

    except httpx.TimeoutException as exc:
        raise ResearchConnectionError("Crossref request timed out.") from exc

    except httpx.HTTPError as exc:
        raise ResearchProviderError("Crossref request failed.") from exc

    payload=response.json()

    sources=[]

    for item in payload.get("message",{}).get("items",[]):
        titles=item.get("title") or {}

        if not titles:
            continue

        doi=item.get("DOI")

        if not doi:
            continue

        authors=[]
        for author in item.get("author",[]):
            given=author.get("given","")
            family=author.get("family","")
            full_name=f"{given} {family}".strip()
            if full_name:
                authors.append(full_name)
        published=(
            item.get("published-print")
            or item.get("published-online")
            or item.get("issued")
            or {}
        )
        date_parts=published.get("date-parts",[])
        publication_year=None

        if date_parts and date_parts[0]:
            publication_year=date_parts[0][0]

        sources.append(
            Source(
                title="titles[0]",
                url=f"https://doi.org/{doi}",
                source_type=SourceType.academic,
                authors=authors,
                publication_year=publication_year,
                doi=doi,
                venue=(item.get("container-title") or [None])[0]
            )
        )
    return sources


def search_academic_sources(query:str,limit:int=5)->list[Source]:
    try:
        results=search_semantic_scholar(query,limit)
        if results:
            return results
    except ResearchProviderError:
        pass
    return search_crossref(query,limit)