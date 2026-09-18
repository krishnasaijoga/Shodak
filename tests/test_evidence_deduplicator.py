from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.research.evidence_deduplicator import deduplicate_evidence


def test_duplicate_claim_is_removed():
    first = Evidence(
        claim="Retrieval quality affects answer quality",
        supporting_text="Retrieval quality affects answer quality",
        citation=Citation(
            source_title="Paper One",
            source_url="https://example.com/1",
        ),
        confidence=0.6,
    )

    second = Evidence(
        claim="  retrieval quality affects answer quality  ",
        supporting_text="Similar evidence",
        citation=Citation(
            source_title="Paper Two",
            source_url="https://example.com/2",
        ),
        confidence=0.7,
    )

    result = deduplicate_evidence([first, second])

    assert len(result) == 1


def test_unique_claims_are_preserved():
    first = Evidence(
        claim="Retrieval quality affects answer quality",
        supporting_text="Evidence one",
        citation=Citation(
            source_title="Paper One",
            source_url="https://example.com/1",
        ),
        confidence=0.6,
    )

    second = Evidence(
        claim="Poor retrieval can increase hallucinations",
        supporting_text="Evidence two",
        citation=Citation(
            source_title="Paper Two",
            source_url="https://example.com/2",
        ),
        confidence=0.7,
    )

    result = deduplicate_evidence([first, second])

    assert len(result) == 2