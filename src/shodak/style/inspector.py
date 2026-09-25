from shodak.models.style import StyleDocumentType
from shodak.style.profile import StyleProfile


def describe_style_profile(
        document_type:StyleDocumentType,
        profile:StyleProfile
)->str:
    lines=[
        f"Style type: {document_type.value}",
        f"Documents analyzed: {profile.document_count}",
        f"Average sentence length: {profile.average_sentence_length:.2f} words",
        f"Average paragraph length: {profile.average_paragraph_length:.2f} words",
        f"Vocabulary richness: {profile.vocabulary_richness:.3f}",
        f"First-person frequency: {profile.first_person_frequency:.3f}",
        f"Question Frequency: {profile.question_frequency:.3f}",
        f"Exclamation frequency: {profile.exclamation_frequency:.3f}"
    ]
    return "\n".join(lines)