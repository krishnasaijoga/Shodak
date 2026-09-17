import httpx

from shodak.models.source import Source, SourceType


SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def search_semantic_scholar(query:str, limit:int=5)->list[Source]:
    params={
        "query":query,
        "limit":limit,
        "fields":"title,url,authors,year,abstract,venue,citationCount,externalIds"
    }

    response=httpx.get(
        SEMANTIC_SCHOLAR_URL, params=params,timeout=20.0
    )

    payload=response.json()

    sources=[]
    for paper in payload.get("data",[]):
        external_ids=paper.get("externalIds") or {}
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