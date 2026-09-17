from shodak.models.source import Source, SourceProvider, SourceType
from shodak.research.evidence import extract_evidence_from_source


def test_extract_evidence_from_abstract():
    source=Source(
        title="Example Paper",
        url="https://example.com/paper",
        source_type=SourceType.academic,
        provider=SourceProvider.semantic_scholar,
        authors=["Joga Krishna"],
        publication_year=2025,
        abstract=(
            "Retrieval augmented generation can improve access to external knowledge. "
            "Several studies report reductions in unsupported model responses when "
            "retrieval quality is high."
        )
    )
    evidence=extract_evidence_from_source(source)
    assert len(evidence)>0
    assert evidence[0].source_title=="Example Paper"



def test_source_without_abstract_returns_no_evidence():
    source=Source(
        title="No Abstract",
        url="https://example.com/no-abstract",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref
    )
    evidence=extract_evidence_from_source(source)
    assert evidence == []