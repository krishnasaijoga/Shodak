from shodak.evaluation.hallucination import evaluate_hallucination
from shodak.models.citation import Citation
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.evidence import Evidence
from shodak.models.writing import OutputType


def test_supported_section_has_low_hallucination_risk():
    evidence = [
        Evidence(
            claim="Retrieval improves access to external knowledge.",
            supporting_text="Supporting evidence.",
            citation=Citation(
                source_title="RAG Paper",
                source_url="https://example.com/rag",
            ),
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
                    "Retrieval systems improve access "
                    "to external knowledge."
                ),
                citations=[],
            )
        ],
    )
    result=evaluate_hallucination(
        draft=draft,
        evidence_items=evidence
    )
    assert result.supported_sections==1
    assert result.unsupported_sections==0
    assert result.hallucination_risk==0.0
    assert result.flagged_sections==[]



def test_unsupported_section_is_flagged():
    evidence = [
        Evidence(
            claim="Retrieval improves access to external knowledge.",
            supporting_text="Supporting evidence.",
            citation=Citation(
                source_title="RAG Paper",
                source_url="https://example.com/rag",
            ),
            confidence=0.9,
        )
    ]
    draft = WritingDraft(
        output_type=OutputType.blog,
        title="RAG",
        sections=[
            DraftSection(
                heading="Cost",
                content=(
                    "RAG reduces inference cost "
                    "by seventy percent."
                ),
                citations=[],
            )
        ],
    )
    result=evaluate_hallucination(draft=draft,evidence_items=evidence)
    assert result.supported_sections==0
    assert result.unsupported_sections==1
    assert result.hallucination_risk==1.0
    assert result.flagged_sections==["Cost"]


def test_mixed_draft_hallucination_risk():
    evidence = [
        Evidence(
            claim="Retrieval improves access to external knowledge.",
            supporting_text="Supporting evidence.",
            citation=Citation(
                source_title="RAG Paper",
                source_url="https://example.com/rag",
            ),
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
                citations=[],
            ),
            DraftSection(
                heading="Performance",
                content=(
                    "RAG guarantees perfect accuracy "
                    "for every language model."
                ),
                citations=[],
            ),
        ],
    )
    result=evaluate_hallucination(
        draft=draft,evidence_items=evidence
    )
    assert result.supported_sections==1
    assert result.unsupported_sections==1
    assert result.hallucination_risk==0.5
    assert result.flagged_sections==["Performance"]