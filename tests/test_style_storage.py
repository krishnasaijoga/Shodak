from pathlib import Path

from shodak.models.style import StyleDocumentType
from shodak.style.profile import StyleProfile
from shodak.style.storage import load_style_profile, save_style_profile


def test_save_and_load_style_profiles(tmp_path:Path):
    profiles={
        StyleDocumentType.blog:StyleProfile(
            document_count=2,
            average_sentence_length=14.5,
            average_paragraph_length=65.0,
            vocabulary_richness=0.72,
            first_person_frequency=0.05,
            question_frequency=0.12,
            exclamation_frequency=0.02
        )
    }
    file_path=tmp_path/"style_profiles.json"
    save_style_profile(
        profiles,
        file_path
    )
    loaded=load_style_profile(file_path)
    assert StyleDocumentType.blog in loaded
    assert loaded[StyleDocumentType.blog].document_count==2
    assert loaded[StyleDocumentType.blog].average_sentence_length>0


def test_missing_style_profile_file_returns_empty(tmp_path:Path):
    file_path=tmp_path/"missing.json"
    loaded=load_style_profile(file_path)
    assert loaded=={}