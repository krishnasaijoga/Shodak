from unittest.mock import patch

import pytest

from shodak.cli import main
from shodak.startup import StartupCheckResult


def test_research_command():
    with (
        patch("sys.argv", ["shodak", "research", "retrieval augmented generation"]),
        patch(
            "shodak.cli._run_research",
        ) as mock_run,
    ):
        main()
    mock_run.assert_called_once()

    args = mock_run.call_args.args[0]

    assert args.command == "research"

    assert args.topic == "retrieval augmented generation"

    assert args.depth == "standard"

    assert args.max_sources == 10


def test_run_command():
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
                "500",
            ],
        ),
        patch("shodak.cli._run_workflow") as mock_run,
    ):
        main()

    mock_run.assert_called_once()

    args = mock_run.call_args.args[0]

    assert args.command == "run"

    assert args.output_type == "blog"

    assert args.target_word_count == 500


def test_invalid_output_type():
    with (
        patch(
            "sys.argv",
            ["shodak", "run", "retrieval augmented generation", "--output-type", "invalid"],
        ),
        pytest.raises(SystemExit),
    ):
        main()


def test_run_command_with_output():
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
                "result.md",
            ],
        ),
        patch("shodak.cli._run_workflow") as mock_run,
    ):
        main()
    args = mock_run.call_args.args[0]
    assert args.output == "result.md"


def test_research_command_with_output():
    with (
        patch(
            "sys.argv",
            ["shodak", "research", "retrieval augmented generation", "--output", "research.json"],
        ),
        patch("shodak.cli._run_research") as mock_run,
    ):
        main()
    args = mock_run.call_args.args[0]
    assert args.output == "research.json"


def test_cli_check_success(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["shodak", "check"])

    with patch("shodak.cli.run_startup_checks", return_value=StartupCheckResult(healthy=True)):
        main()

    output = capsys.readouterr().out

    assert "healthy" in output


def test_cli_check_failure(monkeypatch):
    monkeypatch.setattr("sys.argv", ["shodak", "check"])

    with (
        patch(
            "shodak.cli.run_startup_checks",
            return_value=StartupCheckResult(
                healthy=False, errors=["No LLM provider API key is configured."]
            ),
        ),
        pytest.raises(SystemExit) as exc,
    ):
        main()

    assert exc.value.code == 1

def test_cli_run_without_llm(capsys):
    fake_result = {
        "rendered_output": (
            "# Retrieval Augmented Generation\n\n"
            "Test output."
        ),
        "evaluation_scorecard": None,
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
            ],
        ),
        patch(
            "shodak.cli.build_workflow"
        ) as mock_build_workflow,
    ):
        mock_workflow = (
            mock_build_workflow.return_value
        )

        mock_workflow.invoke.return_value = (
            fake_result
        )

        main()

    captured = capsys.readouterr()

    assert "Test output" in captured.out