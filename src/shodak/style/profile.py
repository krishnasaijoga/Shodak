from pydantic import BaseModel

from shodak.models.style import StyleDocument
from shodak.style.features import StyleFeatures, extract_style_features


class StyleProfile(BaseModel):
    document_count:int
    average_sentence_length:float
    average_paragraph_length:float
    vocabulary_richness:float
    first_person_frequency:float
    question_frequency:float
    exclamation_frequency:float



def build_style_profile(
        documents:list[StyleDocument]
)->StyleProfile:
    if not documents:
        return StyleProfile(document_count=0,average_sentence_length=0,average_paragraph_length=0,vocabulary_richness=0,first_person_frequency=0,question_frequency=0,exclamation_frequency=0)
    features:list[StyleFeatures]=[
        extract_style_features(document.content) for document in documents
    ]
    count=len(features)
    return StyleProfile(
        document_count=count,
        average_sentence_length=sum(item.average_sentence_length for item in features)/count,
        average_paragraph_length=sum(item.average_paragraph_length for item in features)/count,
        vocabulary_richness=sum(item.vocabulary_richness for item in features)/count,
        first_person_frequency=sum(item.first_person_frequency for item in features)/count,
        question_frequency=sum(item.question_frequency for item in features)/count,
        exclamation_frequency=sum(item.exclamation_frequency for item in features)/count
    )