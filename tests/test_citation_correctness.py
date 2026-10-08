from shodak.evaluation.citation_correctness import evaluate_citation_correctness
from shodak.models.citation import Citation
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.evidence import Evidence
from shodak.models.writing import OutputType


def test_correct_citation():
    citation=Citation(
        source_title="RAG Paper",
        source_url="https://example.com/rag",
    )
    evidence = [
        Evidence(
            claim=(
                "Retrieval improves access "
                "to external knowledge."
            ),
            supporting_text="Supporting evidence.",
            citation=citation,
            confidence=0.9,
        )
    ]
    draft=WritingDraft(
        output_type=OutputType.blog,
        title="RAG",
        sections=[
            DraftSection(
                heading="Introduction",
                content=(
                    "Retrieval systems can improve "
                    "access to external knowledge."
                ),
                citations=[citation],
            )
        ],
    )
    result=evaluate_citation_correctness(draft=draft,evidence_item=evidence)

    assert result.correct_citations==1
    assert result.total_citations==1
    assert result.citation_correctness_score==1.0
    assert result.incorrect_sections==[]


def test_incorrect_citation():
    citation=Citation(
        source_title="Transformer Paper",
        source_url="https://example.com/transformer",
    )
    evidence = [
        Evidence(
            claim="Transformers use attention mechanisms.",
            supporting_text="Supporting evidence.",
            citation=citation,
            confidence=0.9,
        )
    ]

    draft = WritingDraft(
        output_type=OutputType.blog,
        title="RAG",
        sections=[
            DraftSection(
                heading="Introduction",
                content=(
                    "Retrieval improves access "
                    "to external knowledge."
                ),
                citations=[citation],
            )
        ],
    )
    result=evaluate_citation_correctness(draft=draft,evidence_item=evidence)
    assert result.correct_citations==0
    assert result.total_citations==1
    assert result.citation_correctness_score==0.0
    assert result.incorrect_sections==["Introduction"]