from pathlib import Path

from shodak.models.style import StyleDocument, StyleDocumentType


def load_text_file(
        file_path:str|Path,
        document_type:StyleDocumentType
)-> StyleDocument:
    path=Path(file_path)
    content=path.read_text(encoding="utf-8")
    return StyleDocument(
        title=path.stem,
        document_type=document_type,
        content=content.strip(),
        source_path=str(path)
    )