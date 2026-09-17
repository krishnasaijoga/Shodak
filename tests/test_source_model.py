from shodak.models.source import Source, SourceType


def test_valid_academic_source():
    source=Source(
        title="Attention Is All You Need",
        url="https://arxiv.org/abs/1706.03762",
        source_type=SourceType.academic,
        authors=["Asish Vaswani"],
        publication_year=2017
    )
    assert source.source_type==SourceType.academic
    assert source.publication_year==2017