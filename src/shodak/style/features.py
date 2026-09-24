import re

from pydantic import BaseModel


class StyleFeatures(BaseModel):
    average_sentence_length:float
    average_paragraph_length:float
    vocabulary_richness:float
    first_person_frequency:float
    question_frequency:float
    exclamation_frequency:float



def extract_style_features(text:str)->StyleFeatures:
    words=re.findall(r"\b\w+\b",text.lower())
    total_words=len(words)

    sentences=[
        sentence.strip() for sentence in re.split(r"[.!?]+",text) if sentence.strip()
    ]

    paragraphs=[
        paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()
    ]

    average_sentence_length=(total_words/len(sentences) if sentences else 0.0)
    paragraph_word_counts=[len(re.findall(r"\b\w+\b",paragraph)) for paragraph in paragraphs]
    average_paragraph_length=(
        sum(paragraph_word_counts)/len(paragraph_word_counts) if paragraph_word_counts else 0.0
    )
    vocabulary_richness=(
        len(set(words))/total_words if total_words else 0.0
    )
    first_person_terms={
        "i",
        "me",
        "my",
        "mine",
        "we",
        "our",
        "ours",
        "us"
    }
    first_person_count=sum(
        word in first_person_terms for word in words
    )
    first_person_frequency=(first_person_count/total_words if total_words else 0.0)
    question_frequency=(text.count("?")/len(sentences) if sentences else 0.0)
    exclamation_frequency=(text.count("!")/len(sentences) if sentences else 0.0)

    return StyleFeatures(
        average_paragraph_length=average_paragraph_length,
        average_sentence_length=average_sentence_length,
        vocabulary_richness=vocabulary_richness,
        first_person_frequency=first_person_frequency,
        question_frequency=question_frequency,
        exclamation_frequency=exclamation_frequency
    )