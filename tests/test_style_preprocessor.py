import pytest

from shodak.models.style import StyleDocument, StyleDocumentType
from shodak.style.preprocessor import chunk_style_document, clean_style_text


def test_clean_style_text():
    text="Hello Krishna, This is \r\n\r\n\r\n a test."
    result=clean_style_text(text)
    assert result=="Hello Krishna, This is \n\n a test."



def test_chunk_style_document():
    document=StyleDocument(
        title="Example",
        document_type=StyleDocumentType.blog,
        content="A"*1500
    )
    chunks=chunk_style_document(document=document,chunk_size=800,overlap=100)
    assert len(chunks)>1


def test_invali_overlap():
    document=StyleDocument(
        title="Example",
        document_type=StyleDocumentType.blog,
        content="Example content"
    )
    with pytest.raises(ValueError):
        chunk_style_document(document,chunk_size=500,overlap=500)