from unittest.mock import MagicMock, patch

import pytest

from shodak.research.academic import search_academic_sources
from shodak.research.retry import ResearchRateLimitError, run_research_with_retry


def test_research_retry_then_success():
    operation = MagicMock()

    operation.side_effect = [ResearchRateLimitError("Rate Limited"), "success"]

    with patch("shodak.research.retry.time.sleep"):
        result = run_research_with_retry(operation, max_attempts=2)
    assert result == "success"
    assert operation.call_count == 2


def test_research_retry_exhausts():
    operation = MagicMock()
    operation.side_effect = ResearchRateLimitError("Rate Limited")

    with patch("shodak.research.retry.time.sleep"), pytest.raises(ResearchRateLimitError):
        run_research_with_retry(operation, max_attempts=3)

    assert operation.call_count == 3


def test_semantic_scholar_retries_before_crossref():
    semantic_result = MagicMock()
    with (
        patch(
            "shodak.research.academic.search_semantic_scholar",
            side_effect=[ResearchRateLimitError("Rate Limited"), semantic_result],
        ) as mock_semantic,
        patch("shodak.research.academic.search_crossref") as mock_crossref,
        patch("shodak.research.retry.time.sleep"),
    ):
        result = search_academic_sources(query="Machine Learning", limit=20)

    assert result == semantic_result
    assert mock_semantic.call_count == 2
    mock_crossref.assert_not_called()


def test_crossref_used_after_semantic_retries_fail():
    crossref_result = MagicMock()

    with (
        patch(
            "shodak.research.academic.search_semantic_scholar",
            side_effect=ResearchRateLimitError("Rate Limited"),
        ),
        patch(
            "shodak.research.academic.search_crossref", return_value=crossref_result
        ) as mock_crossref,
        patch("shodak.research.retry.time.sleep"),
    ):
        result = search_academic_sources(query="MAchine Learning", limit=20)

    assert result == crossref_result
    mock_crossref.assert_called_once()
