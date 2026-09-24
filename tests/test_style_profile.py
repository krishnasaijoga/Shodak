from shodak.models.style import StyleDocument, StyleDocumentType
from shodak.style.profile import build_style_profile


def test_build_style_profile():
    documents=[
        StyleDocument(
            title="Blog One",
            document_type=StyleDocumentType.blog,
            content="I like writing about AI. It is fascinating."
        ),
        StyleDocument(
            title="Blog Two",
            document_type=StyleDocumentType.blog,
            content="We use technology every day. Should we trust it completely?"
        )
    ]
    profile=build_style_profile(documents)
    assert profile.document_count==2
    assert profile.average_sentence_length>0
    assert profile.vocabulary_richness>0


def test_empty_style_profile():
    profile=build_style_profile([])
    assert profile.document_count==0
    assert profile.average_sentence_length==0