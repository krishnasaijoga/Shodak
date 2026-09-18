from datetime import datetime, timedelta, timezone

from shodak.models.source import PublicationStatus, Source

IST=timezone(timedelta(hours=5,minutes=30))


def credibililty_score(source:Source)->float:
    score=0.0
    if source.publication_status==PublicationStatus.peer_reviewed:
        score+=3.0
    elif source.publication_status==PublicationStatus.preprint:
        score+=1.0

    if source.metadata_complete:
        score+=2.0
    if source.has_abstract:
        score+=1.5

    if source.citation_count is not None:
        if source.citation_count>=100:
            score+=2.0
        elif source.citation_count>=25:
            score+=1.5
        elif source.citation_count>0:
            score+=0.5
    if source.publication_year is not None:
        current_year=datetime.now(IST).year
        age=current_year-source.publication_year

        if age<=2:
            score+=1.5
        elif age<=5:
            score+=0.75
    return score