from shodak.evaluation.scorecard import evaluate_output
from tests.fixtures.quality_cases import (
    build_good_blog,
    build_good_report,
    build_incomplete_blog,
    build_unsupported_blog,
    build_wrong_citation_blog,
)


def test_good_blog_scores_high():
    result = evaluate_output(
        draft=build_good_blog(), report=build_good_report(), style_profile=None
    )
    assert result.grounding_score >= 0.8
    assert result.citation_correctness_score >= 0.8
    assert result.hallucination_safety_score >= 0.8
    assert result.format_compliance_score >= 0.8


def test_unsupported_blog_has_low_hallucination_safety():
    result = evaluate_output(
        draft=build_unsupported_blog(), report=build_good_report(), style_profile=None
    )
    assert result.hallucination_safety_score <= 0.5


def test_wrong_citation_scores_low():
    result = evaluate_output(
        draft=build_wrong_citation_blog(), report=build_good_report(), style_profile=None
    )
    assert result.citation_correctness_score <= 0.5


def test_incomplete_blog_has_low_format_score():
    result = evaluate_output(
        draft=build_incomplete_blog(), report=build_good_report(), style_profile=None
    )
    assert result.format_compliance_score <= 0.6
