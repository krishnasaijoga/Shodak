from pydantic import BaseModel, Field

from shodak.models.draft import WritingDraft
from shodak.style.features import extract_style_features
from shodak.style.profile import StyleProfile


class StyleSimilarityResult(BaseModel):
    sentence_length_score:float=Field(ge=0.0,le=1.0)
    paragraph_length_score:float=Field(ge=0.0,le=1.0)
    vocabulary_score:float=Field(ge=0.0,le=1.0)
    first_person_score:float=Field(ge=0.0,le=1.0)
    question_score:float=Field(ge=0.0,le=1.0)
    exclamation_score:float=Field(ge=0.0,le=1.0)
    overall_style_similarity:float=Field(ge=0.0,le=1.0)



def _similarity(actual:float,target:float)->float:
    if actual==0 and target==0:
        return 1.0
    denominator=max(abs(actual),abs(target),1e-6)
    differnece=abs(actual-target)/denominator
    return max(0.0,1.0-differnece)


def evaluate_style_similarity(
        draft:WritingDraft,
        target_profile:StyleProfile
)->StyleSimilarityResult:
    draft_text="\n\n".join(
        section.content for section in draft.sections
    )
    actual=extract_style_features(draft_text)

    sentence_length_score=_similarity(
        actual.average_sentence_length,
        target_profile.average_sentence_length
    )

    paragraph_length_score=_similarity(
        actual.average_paragraph_length,
        target_profile.average_paragraph_length
    )

    vocabulary_score=_similarity(
        actual.vocabulary_richness,
        target_profile.vocabulary_richness
    )

    first_person_score=_similarity(
        actual.first_person_frequency,
        target_profile.first_person_frequency
    )

    question_score=_similarity(
        actual.question_frequency,
        target_profile.question_frequency
    )

    excalamation_score=_similarity(
        actual.exclamation_frequency,
        target_profile.exclamation_frequency
    )

    scores=[
        sentence_length_score,
        paragraph_length_score,
        vocabulary_score,
        first_person_score,
        question_score,
        excalamation_score
    ]

    overall_style_similarity=sum(scores)/len(scores)

    return StyleSimilarityResult(
        sentence_length_score=sentence_length_score,
        paragraph_length_score=paragraph_length_score,
        vocabulary_score=vocabulary_score,
        first_person_score=first_person_score,
        question_score=question_score,
        exclamation_score=excalamation_score,
        overall_style_similarity=overall_style_similarity
    )