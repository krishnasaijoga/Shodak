import argparse

from shodak.graph.workflow import build_workflow
from shodak.models.research import ResearchDepth, ResearchRequest
from shodak.models.writing import OutputType, WritingRequest
from shodak.output.exporter import export_output
from shodak.research.report import build_research_report


def _build_parser()->argparse.ArgumentParser:
    parser=argparse.ArgumentParser(
        prog="shodak",
        description="Shodak research and writing assistant."
    )

    subparsers=parser.add_subparsers(
        dest="command",
        required=True
    )

    research_parser=subparsers.add_parser(
        "research",
        help="Research a topic."
    )

    research_parser.add_argument(
        "topic",
        type=str
    )

    research_parser.add_argument(
        "--depth",
        choices=[
            item.value for item in ResearchDepth
        ],
        default=ResearchDepth.standard.value
    )

    research_parser.add_argument(
        "--max-sources",
        type=int,
        default=10
    )

    run_parser=subparsers.add_parser(
        "run",
        help="Run the complete Shodak workflow."
    )

    run_parser.add_argument(
        "topic",
        type=str
    )

    run_parser.add_argument(
        "--output-type",
        choices=[
            item.value for item in OutputType
        ],
        default=OutputType.blog.value
    )

    run_parser.add_argument(
        "--depth",
        choices=[
            item.value for item in ResearchDepth
        ],
        default=ResearchDepth.standard.value
    )

    run_parser.add_argument(
        "--max-sources",
        type=int,
        default=10
    )

    run_parser.add_argument(
        "--target-word-count",
        type=int,
        default=800
    )

    run_parser.add_argument(
        "--output",
        type=str,
        default=None,
        help=(
            "Optional output file. "
            "Supported formats: .md, .json"
        )
    )

    research_parser.add_argument(
        "--output",
        type=str,
        default=None,
        help=(
            "Optional research output file."
            "Supported format: .json"
        )
    )

    return parser


def _run_research(args:argparse.Namespace)->None:
    request=ResearchRequest(
        topic=args.topic,
        depth=ResearchDepth(args.depth),
        max_sources=args.max_sources
    )

    report=build_research_report(request)

    research_data={
        "topic":report.request.topic,
        "research_questions":report.research_questions,
        "source_count":len(report.sources),
        "evidence_count":len(report.evidence),
        "coverage_score":report.quality.coverage_score,
        "sufficient_evidence":report.quality.sufficient_evidence,
        "evidence":[
            {
                "claim":item.claim,
                "supporting_text":item.supporting_text,
                "source_title":item.citation.source_title,
                "source_url":item.citation.source_url,
                "confidence":item.confidence
            }
            for item in report.evidence
        ]
    }

    print(f"\nTopic: {report.request.topic}")
    print(f"Sources: {len(report.sources)}")
    print(f"Evidence: {len(report.evidence)}")
    print(f"Coverage: {report.quality.coverage_score:.2f}")

    print("\nResearch Questions:")

    for index, question in enumerate(report.research_questions,start=1):
        print(f"{index}. {question}")
    print("\nEvidence:")
    for index, evidence in enumerate(report.evidence,start=1):
        print(f"{index}. {evidence.claim}")
        print(f"Source:     {evidence.citation.source_title}")
        print(f"Confidence:     {evidence.confidence:.2f}")

    if args.output:
        if not args.output.lower().endswith(".json"):
            raise ValueError("Research export currently supports only .json")
        path=export_output(
            output_path=args.output,
            markdown_content="",
            json_data=research_data
        )
        print(f"\nSaved Research to: {path}")



def _run_workflow(args:argparse.Namespace)->None:
    research_request=ResearchRequest(
        topic=args.topic,
        depth=ResearchDepth(args.depth),
        max_sources=args.max_sources
    )
    writing_request=WritingRequest(
        output_type=OutputType(args.output_type),
        target_word_count=args.target_word_count
    )

    workflow=build_workflow()
    result=workflow.invoke(
        {
            "research_request":research_request,
            "writing_request":writing_request,
            "revision_count":0
        }
    )
    rendered_output=result["rendered_output"]

    scorecard=result["evaluation_scorecard"]

    export_data={
        "topic":research_request.topic,
        "output_type":writing_request.output_type.value,
        "content":rendered_output,
        "evaluation":scorecard.model_dump()
    }

    print("\n")
    print(rendered_output)

    print("\n---------Quality Scorecard----------")
    print(f"Grounding: {scorecard.grounding_score:.2f}")
    print(f"Citation correctness: {scorecard.citation_correctness_score:.2f}")
    print(f"Hallucination safety: {scorecard.hallucination_safety_score:.2f}")
    print(f"Style similarity: {scorecard.style_similarity_score:.2f}")
    print(f"Format compliance: {scorecard.format_compliance_score:.2f}")
    print(f"Research Quality: {scorecard.research_quality_score:.2f}")
    print(f"Overall quality: {scorecard.overall_quality_score:.2f}")

    if args.output:
        output_path=export_output(
            output_path=args.output,
            markdown_content=rendered_output,
            json_data=export_data
        )

        print(f"\nSaved output to: {output_path}")



def main()->None:
    parser=_build_parser()
    args=parser.parse_args()

    if args.command=="research":
        _run_research(args)
    elif args.command=="run":
        _run_workflow(args)


if __name__=="__main__":
    main()