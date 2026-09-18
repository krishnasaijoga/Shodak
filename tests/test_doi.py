from shodak.research.doi import normalize_doi


def test_plain_doi():
    assert normalize_doi("10.1234/example") == "10.1234/example"


def test_https_doi():
    assert (
        normalize_doi("https://doi.org/10.1234/Example")
        == "10.1234/example"
    )


def test_doi_prefix():
    assert normalize_doi("DOI: 10.1234/Example") == "10.1234/example"


def test_none_doi():
    assert normalize_doi(None) is None