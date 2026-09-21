from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.research.contradictions import detect_contradictions


def test_potential_contradiction_is_detected():
    positive=Evidence(
        claim="Retrieval improves answer quality in language models",
        supporting_text="Evidence supporting improvement.",
        citation=Citation(
            source_title="Paper One",
            source_url="https://example.com/1",
        ),
        confidence=0.7,
    )
    negative = Evidence(
        claim="Retrieval does not improve answer quality in language models",
        supporting_text="Evidence showing no improvement.",
        citation=Citation(
            source_title="Paper Two",
            source_url="https://example.com/2",
        ),
        confidence=0.7,
    )
    result=detect_contradictions([positive,negative])
    assert len(result)==1


def test_unrelated_claims_are_not_contradictions():
    first = Evidence(
        claim="Retrieval improves answer quality",
        supporting_text="Evidence one.",
        citation=Citation(
            source_title="Paper One",
            source_url="https://example.com/1",
        ),
        confidence=0.6,
    )

    second = Evidence(
        claim="Transformers use attention mechanisms",
        supporting_text="Evidence two.",
        citation=Citation(
            source_title="Paper Two",
            source_url="https://example.com/2",
        ),
        confidence=0.6,
    )
    result=detect_contradictions([first,second])
    assert result==[]