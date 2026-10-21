import json

import pytest

from shodak.output.exporter import export_json, export_markdown, export_output


def test_report_markdown(tmp_path):
    output = tmp_path / "result.md"
    export_markdown("# Example\n\nContent.", output)

    assert output.exists()

    assert output.read_text(encoding="utf-8") == "# Example\n\nContent."


def test_export_json(tmp_path):
    output = tmp_path / "result.json"

    export_json({"title": "Example", "score": 0.9}, output)

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["title"] == "Example"
    assert data["score"] == 0.9


def test_export_output_rejects_unknown_format(tmp_path):
    output = tmp_path / "result.txt"
    with pytest.raises(ValueError):
        export_output(output_path=output, markdown_content="Example", json_data=[])
