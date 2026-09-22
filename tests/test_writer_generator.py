from shodak.models.citation import Citation
from shodak.models.evidence import Evidence
from shodak.models.report import ResearchQuality, ResearchReport
from shodak.models.research import ResearchRequest
from shodak.models.writing import OutputType, WritingRequest
from shodak.writing.generator import generate_draft


def test_generate_blog_writing():
    report=ResearchReport(
        request=ResearchRequest(
            topic="Retrieval Augmented Generation"
        ),
        research_questions=["What is a Retrieval augmented generator"],
        sources=[],
        evidence=[
            Evidence(
                claim="Retreival augmented generation uses external information sources.",
                supporting_text="Supporting evidence.",
                citation=Citation(
                    source_title="Example Paper",
                    source_url="https://example.com/paper"
                ),
                confidence=0.7
            )
        ],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=True,
            source_count=2,
            evidence_count=2,
            coverage_score=0.5
        )
    )
    request=WritingRequest(
        output_type=OutputType.blog
    )
    draft=generate_draft(report,request)
    assert draft.output_type==OutputType.blog
    assert draft.title=="Retrieval Augmented Generation"
    assert len(draft.sections)>0
    assert draft.sections[0].content


def test_custom_title_is_used():
    report=ResearchReport(
        request=ResearchRequest(
            topic="AI agents"
        ),
        research_questions=[],
        sources=[],
        evidence=[],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=False,
            source_count=0,
            evidence_count=0,
            coverage_score=0.0,
            reason="No evidence available"
        )
    )
    request=WritingRequest(
        output_type=OutputType.linkedin,
        title="Why AI agents matter"
    )
    draft=generate_draft(report,request)
    assert draft.title=="Why AI agents matter"