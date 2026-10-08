from shodak.models.report import ResearchReport
from shodak.models.synthesis import ResearchSynthesis, SynthesizedFinding


def synthesize_research_deterministic(
        report:ResearchReport
)->ResearchSynthesis:
    findings=[
        SynthesizedFinding(
            finding=evidence.claim,
            supporting_evidence_indices=[index],
            confidence=evidence.confidence
        )
        for index, evidence in enumerate(report.evidence[:5])
    ]
    contradictions=[
        item.explanation for item in report.contradictions
    ]
    uncertainties=[]
    if not report.quality.sufficient_evidence:
        uncertainties.append(
            report.quality.reason or "The available evidence is insufficient."
        )
    
    research_gaps=[]
    
    if report.quality.coverage_score<0.5:
        research_gaps.append(
            "The available evidence does not cover enough of the research questions."
        )

    overall_confidence=sum(item.confidence for item in findings)/len(findings) if findings else 0.0
    
    return ResearchSynthesis(
        key_findings=findings,
        uncertainties=uncertainties,
        contradictions=contradictions,
        research_gaps=research_gaps,
        overall_confidence=overall_confidence
    )