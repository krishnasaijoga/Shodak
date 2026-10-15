import json
from unittest.mock import MagicMock, patch

from shodak.cli import main
from shodak.evaluation.scorecard import EvaluationScorecard


def test_cli_run_integration(capsys):
    scorecard=EvaluationScorecard(
        grounding_score=0.9,
        citation_correctness_score=0.9,
        hallucination_safety_score=0.9,
        style_similarity_score=0.8,
        format_compliance_score=1.0,
        research_quality_score=0.8,
        overall_quality_score=0.88
    )

    workflow=MagicMock()

    workflow.invoke.return_value={
        "rendered_output": (
            "# Understanding RAG\n\n"
            "Retrieval improves access "
            "to external knowledge."
        ),
        "evaluation_scorecard": scorecard
    }

    with (
        patch(
            "sys.argv",
            [
                "shodak",
                "run",
                "retrieval augmented generation",
                "--output-type",
                "blog",
                "--target-word-count",
                "500"
            ]
        ),
        patch(
            "shodak.cli.build_workflow",
            return_value=workflow
        )
    ):
        main()
    captured=capsys.readouterr()

    assert "Understanding RAG" in captured.out
    assert "Overall quality" in captured.out

    workflow.invoke.assert_called_once()


def test_cli_run_exports_markdown(tmp_path):
    scorecard=EvaluationScorecard(
        grounding_score=1.0,
        citation_correctness_score=1.0,
        hallucination_safety_score=1.0,
        style_similarity_score=0.9,
        format_compliance_score=1.0,
        research_quality_score=0.9,
        overall_quality_score=0.96
    )

    workflow=MagicMock()

    workflow.invoke.return_value={
        "rendered_output": (
            "# Understanding RAG\n\n"
            "Grounded content."
        ),
        "evaluation_scorecard":scorecard
    }

    output_file=tmp_path/"rag.md"

    with (
        patch(
            "sys.argv",
            [
                "shodak",
                "run",
                "retrieval augmented generation",
                "--output-type",
                "blog",
                "--output",
                str(output_file)
            ]
        ),
        patch(
            "shodak.cli.build_workflow",
            return_value=workflow
        )
    ):
        main()

    assert output_file.exists()

    content=output_file.read_text(encoding="utf-8")
    assert "Understanding RAG" in content


def test_cli_run_exports_json(tmp_path):
    scorecard=EvaluationScorecard(
        grounding_score=1.0,
        citation_correctness_score=1.0,
        hallucination_safety_score=1.0,
        style_similarity_score=0.9,
        format_compliance_score=1.0,
        research_quality_score=0.9,
        overall_quality_score=0.96,
    )

    workflow=MagicMock()
    workflow.invoke.return_value={
        "rendered_output": "# Understanding RAG",
        "evaluation_scorecard": scorecard
    }

    output_file=tmp_path/"rag.json"

    with (
        patch(
            "sys.argv",
            [
                "shodak",
                "run",
                "retrieval augmented generation",
                "--output-type",
                "blog",
                "--output",
                str(output_file)
            ]
        ),
        patch(
            "shodak.cli.build_workflow",
            return_value=workflow
        )
    ):
        main()

    data=json.loads(output_file.read_text(encoding="utf-8"))

    assert data["topic"]=="retrieval augmented generation"

    assert data["output_type"]=="blog"

    assert data["evaluation"]["overall_quality_score"]==0.96