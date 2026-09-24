from shodak.style.features import extract_style_features


def test_extract_style_features():
    text=(
        "I enjoy writing about AI systems. "
        "They can make complex workflows easier to understand.\n\n"
        "But should we trust them completely? "
        "I don't think so!"
    )
    features=extract_style_features(text)

    assert features.average_sentence_length>0
    assert features.average_paragraph_length>0
    assert 0<features.vocabulary_richness<=1
    assert features.first_person_frequency>0
    assert features.question_frequency>0
    assert features.exclamation_frequency>0


def test_empty_text():
    features=extract_style_features("")
    assert features.average_sentence_length==0
    assert features.vocabulary_richness==0