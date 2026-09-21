import pytest
from pydantic import ValidationError

from shodak.models.writing import OutputType, WritingRequest


def test_valid_linkedin_request():
    request=WritingRequest(
        output_type=OutputType.linkedin,
        target_word_count=500
    )
    assert request.output_type==OutputType.linkedin
    assert request.target_word_count==500



def test_default_word_count():
    request=WritingRequest(output_type=OutputType.blog)
    assert request.target_word_count==800


def test_invalid_word_count():
    with pytest.raises(ValidationError):
        WritingRequest(output_type=OutputType.blog, target_word_count=50)