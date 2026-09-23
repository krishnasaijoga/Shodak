from shodak.models.citation import Citation
from shodak.models.contradiction import Contradiction
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



def test_draft_contains_citation():
    report=ResearchReport(
        request=ResearchRequest(
            topic="retrieval augmented generation"
        ),
        research_questions=[],
        sources=[],
        evidence=[
            Evidence(
                claim="Retrieval can improve access to external knowledge.",
                supporting_text="Supporting evidence.",
                citation=Citation(
                    source_title="Example Paper",
                    source_url="https://example.com/paper",
                    doi="10.1234/example"
                ),
                confidence=0.8
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
        output_type=OutputType.blog,
        include_citation=True
    )
    draft=generate_draft(report,request)
    assert len(draft.sections[0].citations)==1
    assert draft.sections[0].citations[0].source_title=="Example Paper"



def test_citations_can_be_disabled():
    report=ResearchReport(
        request=ResearchRequest(
            topic="retrieval augmented generation"
        ),
        research_questions=[],
        sources=[],
        evidence=[
            Evidence(
                claim="Retrieval improves knowledge access.",
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
        output_type=OutputType.linkedin,
        include_citation=False
    )
    draft=generate_draft(report,request)
    assert draft.sections[0].citations==[]



def test_writer_handles_insufficient_evidence():
    report=ResearchReport(
        request=ResearchRequest(
            topic="Experimental AI system"
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
            reason="Too little supporting evidence was extracted."
        )
    )
    request=WritingRequest(output_type=OutputType.blog)
    draft=generate_draft(report,request)
    assert len(draft.sections)==1
    assert draft.sections[0].heading=="Research Limitation"
    assert "insufficient" in draft.sections[0].content.lower()


def test_writer_surfaces_conflicting_evidence():
    evidence_a=Evidence(
        claim="Retrieval improves answer quality.",
        supporting_text="Supporting evidence A.",
        citation=Citation(
            source_title="Paper One",
            source_url="https://example.com/"
        ),
        confidence=0.8
    )
    evidence_b = Evidence(
        claim="Retrieval does not improve answer quality.",
        supporting_text="Supporting evidence B.",
        citation=Citation(
            source_title="Paper Two",
            source_url="https://example.com/2",
        ),
        confidence=0.8,
    )
    report=ResearchReport(
        request=ResearchRequest(
            topic="retrieval augmented generation"
        ),
        research_questions=[],
        sources=[],
        evidence=[evidence_a, evidence_b],
        contradictions=[
            Contradiction(
                topic="Retrieval effectiveness",
                evidence_a=evidence_a,
                evidence_b=evidence_b,
                explanation="The sources reach conflicting conclusions."
            )
        ],
        quality=ResearchQuality(sufficient_evidence=True,source_count=0,evidence_count=0,coverage_score=0.0)
    )
    request=WritingRequest(output_type=OutputType.blog)
    draft=generate_draft(report,request)
    headings=[section.heading for section in draft.sections]
    assert "Conflicting Evidence" in headings