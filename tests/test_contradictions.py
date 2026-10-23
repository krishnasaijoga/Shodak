
from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.research.contradictions import (
    detect_contradictions,
)


def test_potential_contradiction_is_detected():
    positive = Evidence(
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
    result = detect_contradictions([positive, negative])
    assert len(result) == 1


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
    result = detect_contradictions([first, second])
    assert result == []


def test_complimentary_claims_are_not_marked_as_contradiction():
    evidence=[
        Evidence(
            claim=(
                "RAG systems are composed of a retrieval "
                "module and an LLM-based generation module."
            ),
            supporting_text=(
                "RAG systems are composed of a retrieval "
                "module and an LLM-based generation module."
            ),
            citation=Citation(
                source_title="RAGAs",
                source_url="https://example.com/ragas"
            ),
            confidence=0.6
        ),
        Evidence(
            claim=(
                "RAG combines parametric memory with "
                "non-parametric memory for language generation."
            ),
            supporting_text=(
                "RAG combines parametric memory with "
                "non-parametric memory for language generation."
            ),
            citation=Citation(
                source_title="Original RAG Paper",
                source_url="https://example.com/rag"
            ),
            confidence=0.6
        )
    ]

    contradictions=detect_contradictions(evidence)

    assert contradictions==[]


def test_conflicting_claims_are_marked_as_contradiction():
    evidence=[
        Evidence(
            claim="Method A improves model accuracy.",
            supporting_text=(
                "Method A improves model accuracy."
            ),
            citation=Citation(
                source_title="Paper One",
                source_url="https://example.com/1"
            ),
            confidence=0.8
        ),
        Evidence(
            claim="Method A does not improve model accuracy.",
            supporting_text="Method A does not improve model accuracy.",
            citation=Citation(
                source_title="Paper Two",
                source_url="https://example.com/2"
            ),
            confidence=0.8
        )
    ]

    contradictions=detect_contradictions(evidence)

    assert len(contradictions)==1