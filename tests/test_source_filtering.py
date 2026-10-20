from shodak.models.source import Source, SourceProvider, SourceType
from shodak.research.filtering import filter_low_value_sources, is_low_value_score


def make_source(
        title:str
)->Source:
    return Source(
        title=title,
        url="https://example.com",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref
    )


def test_filters_low_value_titles():
    sources=[
        make_source("Front Matter"),
        make_source("Index"),
        make_source("List of Authors"),
        make_source("Useful Machine Learning Paper")
    ]

    result=filter_low_value_sources(sources)

    assert len(result)==1
    assert result[0].title=="Useful Machine Learning Paper"


def test_low_value_filter_is_case_insensitive():
    source=make_source("   FRONT Matter   ")

    assert is_low_value_score(source) is True


def test_research_paper_is_not_filtered():
    source=make_source("Machine Learning with sklearn")

    assert is_low_value_score(source) is False