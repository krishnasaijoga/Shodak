from datetime import timedelta, timezone

from shodak.models.source import Source
from shodak.research.credibility import credibililty_score

IST=timezone(timedelta(hours=5,minutes=30))


def score_source(source:Source)->float:
    return credibililty_score(source)


def rank_sources(sources:list[Source])->list[Source]:
    return sorted(
        sources,
        key=score_source,
        reverse=True
    )