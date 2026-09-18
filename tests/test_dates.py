from datetime import date

from shodak.research.dates import build_publication_date


def test_full_publication_date():
    result=build_publication_date(2025,6,3)
    assert result==date(2025,6,3)



def test_year_only_defaults_to_january_first():
    result=build_publication_date(2025)
    assert result==date(2025,1,1)


def test_missing_year_returns_none():
    assert build_publication_date(None) is None


def test_invalid_date_falls_back_to_year_start():
    result = build_publication_date(2025, 13, 50)
    assert result == date(2025, 1, 1)