from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.research.coverage import calculate_research_coverage, question_is_covered


def make_evidence(claim:str)->Evidence:
    return Evidence(
        claim=claim,
        supporting_text=claim,
        citation=Citation(
        source_title="Example Paper",
        source_url="https://example.com/paper",
        ),
        confidence=0.7
    )


def test_question_is_covered():
    evidence=[
        make_evidence("Retrieval augmented generation improves access to external knowledge")
    ]
    result=question_is_covered(
        "how does retrieval augmented generation use external knowledge?",
        evidence
    )
    assert result is True


def test_unrelated_question_is_not_covered():
    evidence = [
        make_evidence(
            "Retrieval augmented generation improves external knowledge access"
        )
    ]

    result = question_is_covered(
        "What are the benefits of convolutional neural networks?",
        evidence,
    )
    assert result is False


def test_coverage_score():
    questions=[
        "How does retrieval augmented generation use external knowledge?",
        "What are the risks of autonomous vehicles?"
    ]
    evidence=[
        make_evidence(
            "Retrieval augmented generation improves access to external knowledge"
        )
    ]
    score=calculate_research_coverage(questions,evidence)
    assert score==0.5