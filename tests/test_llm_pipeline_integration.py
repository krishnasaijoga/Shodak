from unittest.mock import patch

from shodak.graph.workflow import build_workflow
from shodak.models.citation import Citation
from shodak.models.draft import WritingDraft
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport
from shodak.models.research import ResearchRequest
from shodak.models.source import Source, SourceProvider, SourceType
from shodak.models.synthesis import ResearchSynthesis, SynthesizedFinding
from shodak.models.writing import OutputType, WritingRequest
from shodak.writing.llm_writer import GeneratedDraft, GeneratedSection


def test_full_llm_pipeline():
    research_request=ResearchRequest(
        topic="retrieval augmented generation"
    )
    writing_request=WritingRequest(
        output_type=OutputType.blog,
        target_word_count=500
    )
    source=Source(
        title="Example RAG Paper",
        url="https://example.com/rag-paper",
        source_type=SourceType.academic,
        provider=SourceProvider.crossref,
        authors=["Krishna Joga"],
        publication_year=2019,
        abstract="Retrieval augmented generation can improve access to external knowledge."
    )
    evidence=[
        Evidence(
            claim="Retrieval augmented generation can improve access to external knowledge.",
            supporting_text="The study found that retrieval gives models access to external knowledge.",
            citation=Citation(
                source_title="Example RAG Paper",
                source_url="https://example.com/rag-paper",
                publication_year=2019
            ),
            confidence=0.9
        ),
        Evidence(
            claim="Retrieval augmented generation can improve access to external knowledge.",
            supporting_text="The study found that retrieval gives models access to external knowledge.",
            citation=Citation(
                source_title="Example RAG paper 2",
                source_url="https://example.com/rag-paper2",
                publication_year=2019
            ),
            confidence=0.9
        )
    ]
    report=ResearchReport(
        request=research_request,
        research_questions=["How does retrieval augmented generation use external knowledge?"],
        sources=[source],
        evidence=evidence,
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=2,
            evidence_count=2,
            coverage_score=0.8
        )
    )

    synthesis=ResearchSynthesis(
        key_findings=[
            SynthesizedFinding(
                finding="Retrieval augmented generation can improve access to external knowledge.",
                supporting_evidence_indices=[0],
                confidence=0.9
            ),
        ],
        uncertainties=["Performance depends on retrieval quality."],
        contradictions=[],
        research_gaps=["More evidence is needed across different domains."],
        overall_confidence=0.9
    )

    generated_draft=GeneratedDraft(
        title="Understanding Retrieval Augmented Generation",
        sections=[
            GeneratedSection(
                heading="Introduction",
                content="Retrieval augmented generation can improve access to external knowledge by connecting language models with retrieved information."
            ),
            GeneratedSection(
                heading="Conclusion",
                content="The available evidence suggests that retrieval can improve access to external knowledge, although it's effectiveness depends on retrieval quality."
            )
        ]
    )

    with (
        patch("shodak.graph.nodes.build_research_report",return_value=report),
        patch("shodak.graph.nodes.synthesize_research_with_fallback", return_value=synthesis),
        patch("shodak.writing.llm_writer.invoke_structured_with_fallback", return_value=generated_draft),
        patch("shodak.graph.style_context.load_style_corpus",return_value=[])
    ):
        workflow=build_workflow()
        result=workflow.invoke(
            {
                "research_request":research_request,
                "writing_request":writing_request
            }
        )
    assert result["research_report"]==report
    assert result["research_synthesis"]==synthesis
    assert isinstance(
        result["writing_draft"], WritingDraft
    )
    assert result["writing_draft"].title=="Understanding Retrieval Augmented Generation"
    assert "rendered_output" in result
    assert result["rendered_output"]
    assert (
        "Understanding Retrieval Augmented Generation" in result["rendered_output"]
    )
    draft=result["writing_draft"]
    assert len(draft.sections)==2
    introduction=draft.sections[0]
    assert len(introduction.citations)>=1
    assert introduction.citations[0].source_title=="Example RAG Paper"
    assert not result.get("error")