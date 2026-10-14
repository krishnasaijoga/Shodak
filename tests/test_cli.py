from unittest.mock import patch

import pytest

from shodak.cli import main


def test_research_command():
    with(
        patch(
            "sys.argv",
            [
                "shodak",
                "research",
                "retrieval augmented generation"
            ]
        ),
        patch(
            "shodak.cli._run_research",
        ) as mock_run
    ):
        main()
    mock_run.assert_called_once()

    args=mock_run.call_args.args[0]

    assert args.command=="research"

    assert args.topic=="retrieval augmented generation"

    assert args.depth=="standard"

    assert args.max_sources==10


def test_run_command():
    with(
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
        patch("shodak.cli._run_workflow") as mock_run
    ):
        main()

    mock_run.assert_called_once()

    args=mock_run.call_args.args[0]

    assert args.command=="run"

    assert args.output_type == "blog"

    assert args.target_word_count == 500


def test_invalid_output_type():
    with patch(
        "sys.argv",
        [
            "shodak",
            "run",
            "retrieval augmented generation",
            "--output-type",
            "invalid"
        ]
    ), pytest.raises(SystemExit):
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
                "result.md"
            ]
        ),
        patch(
            "shodak.cli._run_workflow"
        ) as mock_run
    ):
        main()
    args=mock_run.call_args.args[0]
    assert args.output=="result.md"


def test_research_command_with_output():
    with (
        patch(
            "sys.argv",
            [
                "shodak",
                "research",
                "retrieval augmented generation",
                "--output",
                "research.json"
            ]
        ),
        patch(
            "shodak.cli._run_research"
        ) as mock_run
    ):
        main()
    args=mock_run.call_args.args[0]
    assert args.output=="research.json"