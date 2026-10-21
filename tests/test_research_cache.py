from unittest.mock import patch

from shodak.cache import cache
from shodak.models.report import ResearchQuality, ResearchReport
from shodak.models.research import ResearchRequest
from shodak.research.report import build_research_report


def test_cache_really_stores_value():
    cache.clear()

    cache.set(
        key="abc",
        value="hello",
        ttl_seconds=3600,
    )

    assert cache.get("abc") == "hello"


def test_research_report_uses_cache():
    cache.clear()

    request = ResearchRequest(topic="retrieval augmented generation")

    fake_report = ResearchReport(
        request=request,
        research_questions=[],
        sources=[],
        evidence=[],
        contradictions=[],
        quality=ResearchQuality(
            sufficient_evidence=False,
            source_count=0,
            evidence_count=0,
            coverage_score=0.0,
            reason="Test",
        ),
    )

    with (
        patch(
            "shodak.research.report._build_research_report_uncached", return_value=fake_report
        ) as mock_build,
        patch("shodak.research.report.settings.cache_enabled", True),
    ):
        first = build_research_report(request)
        second = build_research_report(request)
    assert first == fake_report
    assert second == fake_report

    assert mock_build.call_count == 1


def test_different_research_requests_use_different_cache_keys():
    cache.clear()

    request_a = ResearchRequest(topic="retrieval augmented generation")
    request_b = ResearchRequest(topic="transformer attention")

    with (
        patch("shodak.research.report._build_research_report_uncached") as mock_build,
        patch("shodak.research.report.settings.cache_enabled", True),
    ):
        mock_build.side_effect = [
            ResearchReport(
                request=request_a,
                research_questions=[],
                sources=[],
                evidence=[],
                contradictions=[],
                quality=ResearchQuality(
                    sufficient_evidence=False, source_count=0, evidence_count=0, coverage_score=0.0
                ),
            ),
            ResearchReport(
                request=request_b,
                research_questions=[],
                sources=[],
                evidence=[],
                contradictions=[],
                quality=ResearchQuality(
                    sufficient_evidence=False, source_count=0, evidence_count=0, coverage_score=0.0
                ),
            ),
        ]
        build_research_report(request_a)
        build_research_report(request_b)

    assert mock_build.call_count == 2
