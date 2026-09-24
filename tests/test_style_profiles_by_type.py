from shodak.models.style import StyleDocument, StyleDocumentType
from shodak.style.profile import build_style_profiles_by_type


def test_build_profiles_by_document_type():
    documents=[
        StyleDocument(
            title="Blog One",
            document_type=StyleDocumentType.blog,
            content="I enjoy explaining AI through simple examples."
        ),
        StyleDocument(
            title="Blog Two",
            document_type=StyleDocumentType.blog,
            content="We often make technology sound more complicated than it is."
        ),
        StyleDocument(
            title="Research Paper",
            document_type=StyleDocumentType.research_paper,
            content=(
                "The proposed framework was evaluated using a structured "
                "experimental methodology."
            )
        )
    ]
    profiles=build_style_profiles_by_type(documents)

    assert StyleDocumentType.blog in profiles
    assert StyleDocumentType.research_paper in profiles
    assert profiles[StyleDocumentType.blog].document_count==2
    assert profiles[StyleDocumentType.research_paper].document_count==1