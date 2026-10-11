from shodak.evaluation.style_similarity import evaluate_style_similarity
from shodak.models.draft import DraftSection, WritingDraft
from shodak.models.writing import OutputType
from shodak.style.features import extract_style_features
from shodak.style.profile import StyleProfile


def test_identical_style_has_high_similarity():
    text=(
        "I think retrieval systems are useful. "
        "They provide external context to language models."
    )
    features=extract_style_features(text)
    profile=StyleProfile(
        average_sentence_length=features.average_sentence_length,
        average_paragraph_length=features.average_paragraph_length,
        vocabulary_richness=features.vocabulary_richness,
        question_frequency=features.question_frequency,
        exclamation_frequency=features.exclamation_frequency,
        first_person_frequency=features.first_person_frequency,
        document_count=1
    )
    draft=WritingDraft(
        output_type=OutputType.blog,
        title="RAG",
        sections=[
            DraftSection(
                heading="Introduction",
                content=text,
                citations=[]
            )
        ]
    )

    result=evaluate_style_similarity(
        draft=draft,
        target_profile=profile
    )

    assert result.overall_style_similarity==1.0


def test_different_style_has_lower_similarity():
    target_text=(
        "I think this approach is useful. "
        "I often prefer practical examples."
    )
    features=extract_style_features(target_text)
    profile=StyleProfile(
        average_sentence_length=features.average_sentence_length,
        average_paragraph_length=features.average_paragraph_length,
        vocabulary_richness=features.vocabulary_richness,
        first_person_frequency=features.first_person_frequency,
        question_frequency=features.question_frequency,
        exclamation_frequency=features.exclamation_frequency,
        document_count=1
    )
    draft=WritingDraft(
        output_type=OutputType.blog,
        title='RAG',
        sections=[
            DraftSection(
                heading="Introduction",
                content=(
                    "Retrieval augmented generation systems can incorporate "
                    "contextual information from external corpora while "
                    "maintaining generation quality across multiple domains."
                ),
                citations=[],
            )
        ]
    )
    result=evaluate_style_similarity(draft=draft,target_profile=profile)
    assert result.overall_style_similarity<1.0