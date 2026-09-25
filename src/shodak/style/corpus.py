from pathlib import Path

from shodak.models.style import StyleDocument, StyleDocumentType
from shodak.style.loader import load_text_file

FOLDER_TYPE_MAP={
    "blogs":StyleDocumentType.blog,
    "linkedin":StyleDocumentType.linkedin,
    "other":StyleDocumentType.other,
    "research":StyleDocumentType.research_paper
}



def load_style_corpus(
        base_path:str|Path
)->list[StyleDocument]:
    base=Path(base_path)

    documents:list[StyleDocument]=[]
    for folder_name, document_type in FOLDER_TYPE_MAP.items():
        folder=base/folder_name
        if not folder.exists():
            continue
        for file_path in folder.iterdir():
            if file_path.suffix.lower() not in {".txt",".md"}:
                continue
            documents.append(
                load_text_file(
                    file_path=file_path,
                    document_type=document_type
                )
            )
    return documents