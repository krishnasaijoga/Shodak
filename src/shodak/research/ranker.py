from datetime import datetime, timedelta, timezone

from shodak.models.source import Source

IST=timezone(timedelta(hours=5,minutes=30))


def score_source(source:Source)->float:
    score=0.0
    if source.metadata_complete:
        score+=2.0
    if source.has_abstract:
        score+=2.0
    if source.citation_count is not None:
        if source.citation_count>=100:
            score+=3.0
        elif source.citation_count>=25:
            score+=2.0
        elif source.citation_count>0:
            score+=1.0
    if source.publication_year is not None:
        age=datetime.now(IST).year - source.publication_year
        if age<=2:
            score+=2.0
        elif score<=5:
            score+=1.0
    return score


def rank_sources(sources:list[Source])->list[Source]:
    return sorted(
        sources,
        key=score_source,
        reverse=True
    )