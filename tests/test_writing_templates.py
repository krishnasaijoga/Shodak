from shodak.models.writing import OutputType
from shodak.writing.templates import get_writing_template


def test_linkedin_writing():
    template=get_writing_template(OutputType.linkedin)
    assert template[0]=="Hook"
    assert "Takeaway" in template


def test_blog_template():
    template=get_writing_template(OutputType.blog)
    assert "Introduction" in template
    assert "Conclusion" in template


def test_thesis_template_contains_research_gap():
    template=get_writing_template(OutputType.thesis)
    assert "Research Gap" in template