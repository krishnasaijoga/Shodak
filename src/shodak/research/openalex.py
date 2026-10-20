import httpx

from shodak.research.exceptions import ResearchConnectionError, ResearchRateLimitError

OPENALEX_BASE_URL="https://api.openalex.org"


def reconstruct_abstract(
        inverted_index:dict[str,list[int]]|None
)->str|None:
    if not inverted_index:
        return None

    positioned_words:list[tuple[int,str]]=[]

    for word, positions in inverted_index.items():
        for position in positions:
            positioned_words.append((position,word))

    positioned_words.sort(key=lambda item:item[0])

    abstract=" ".join(
        word for _, word in positioned_words
    ).strip()

    return abstract or None


def get_work_by_doi(
        doi:str
)->dict|None:
    normalized_doi=doi.removeprefix("https://doi.org/").strip()

    url=(
        f"{OPENALEX_BASE_URL}/works/"
        f"https://doi.org/{normalized_doi}"
    )

    try:
        response=httpx.get(url,timeout=10.0)
    except httpx.RequestError as exc:
        raise ResearchConnectionError("OpenAlex request failed.") from exc

    if response.status_code==404:
        return None

    if response.status_code==429:
        raise ResearchRateLimitError("OpenAlex rate limit reached.")

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise ResearchConnectionError("OpenAlex request failed.") from exc

    return response.json()


def get_abstract_by_doi(
        doi:str
)->str|None:
    work=get_work_by_doi(doi)

    if not work:
        return None

    inverted_index=work.get("abstract_inverted_index")

    return reconstruct_abstract(inverted_index)