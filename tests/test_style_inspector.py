from shodak.models.style import StyleDocumentType
from shodak.style.inspector import describe_style_profile
from shodak.style.profile import StyleProfile


def test_describe_style_profile():
    profile=StyleProfile(
        document_count=3,
        average_sentence_length=15.5,
        average_paragraph_length=70.2,
        vocabulary_richness=0.65,
        first_person_frequency=0.04,
        question_frequency=0.10,
        exclamation_frequency=0.02
    )
    result=describe_style_profile(StyleDocumentType.blog,profile)
    assert "Style type: blog" in result
    assert "Documents analyzed: 3" in result
    assert "15.50" in result