from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.writing.citation_grounding import find_relevant_citations


def test_relevant_citation_is_found():
    evidence=[
        Evidence(
            claim="Retrieval improves access to external knowledge.",
            supporting_text="Supporting Evidence.",
            citation=Citation(
                source_title="Example Paper",
                source_url="https://example.com/paper"
            ),
            confidence=0.7
        )
    ]
    citations=find_relevant_citations(
        "Retrieval systems can improve access to external knowledge.",
        evidence
    )
    assert len(citations)==1
    assert citations[0].source_title=="Example Paper"


def test_unrelated_evidence_is_not_cited():
    evidence=[
        Evidence(
            claim="Transformers use attention mechanism.",
            supporting_text="Supporting evidence.",
            citation=Citation(
                source_title="Transformer Paper",
                source_url="https://example.com/transformer"
            ),
            confidence=0.7
        )
    ]
    citations=find_relevant_citations(
        "Retrieval systems improve access to external knowledge.",
        evidence
    )
    assert citations==[]