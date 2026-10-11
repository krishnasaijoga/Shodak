import json
from pathlib import Path
from typing import Any


def load_quality_benchmarks(
        path:str|Path="evaluation/quality_benchmarks.json"
)->list[dict[str,Any]]:
    benchmark_path=Path(path)

    with benchmark_path.open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)