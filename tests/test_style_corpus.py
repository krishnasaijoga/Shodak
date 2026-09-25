from pathlib import Path

from shodak.models.style import StyleDocumentType
from shodak.style.corpus import load_style_corpus


def test_load_style_corpus(tmp_path:Path):
    blogs=tmp_path/"blogs"
    research=tmp_path/"research"

    blogs.mkdir()
    research.mkdir()

    (blogs/"blog.txt").write_text("This is my blog style.",encoding="utf-8")
    (research/"Paper.md").write_text("This is my research writing style.",encoding="utf-8")

    documents=load_style_corpus(tmp_path)

    assert len(documents)==2
    types={
        document.document_type for document in documents
    }

    assert StyleDocumentType.blog in types
    assert StyleDocumentType.research_paper in types