import json
from pathlib import Path
from typing import Any


def export_markdown(content:str, output_path:str|Path)->Path:
    path=Path(output_path)

    path.parent.mkdir(parents=True,exist_ok=True)

    path.write_text(content,encoding="utf-8")
    return path


def export_json(data:dict[str,Any], output_path: str|Path)->Path:
    path=Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            data,indent=2,ensure_ascii=True,default=str
        ),
        encoding="utf-8"
    )
    return path


def export_output(
        output_path:str|Path,
        markdown_content:str,
        json_data:dict[str,Any]
)->Path:
    path=Path(output_path)

    suffix=path.suffix.lower()

    if suffix==".md":
        return export_markdown(markdown_content,path)
    if suffix==".json":
        return export_json(json_data,path)

    raise ValueError("Unsupported format.\nUse .md or .json")