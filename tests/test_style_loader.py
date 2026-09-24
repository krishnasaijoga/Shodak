from pathlib import Path

from shodak.models.style import StyleDocumentType
from shodak.style.loader import load_text_file


def test_load_text_file(tmp_path:Path):
    sample_file=tmp_path/"my_blog.txt"
    sample_file.write_text("This is a simple blog written in my style.",encoding="utf-8")
    document=load_text_file(sample_file,StyleDocumentType.blog)

    assert document.title=="my_blog"
    assert document.document_type==StyleDocumentType.blog
    assert "simple blog" in document.content
    assert document.source_path is not None