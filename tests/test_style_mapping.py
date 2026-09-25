from shodak.models.writing import OutputType
from shodak.style.mapping import get_style_document_type
from shodak.style.profile import StyleDocumentType


def test_linkedin_maps_to_linkedin_style():
    result=get_style_document_type(OutputType.linkedin)
    assert result==StyleDocumentType.linkedin


def test_blog_maps_to_blog_style():
    result=get_style_document_type(OutputType.blog)
    assert result==StyleDocumentType.blog


def test_academic_maps_to_research_paper_style():
    result=get_style_document_type(OutputType.academic)
    assert result==StyleDocumentType.research_paper


def test_thesis_maps_to_research_paper_style():
    result=get_style_document_type(OutputType.thesis)
    assert result==StyleDocumentType.research_paper