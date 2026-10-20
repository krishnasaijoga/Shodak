from unittest.mock import MagicMock, patch

from shodak.research.openalex import get_abstract_by_doi, reconstruct_abstract


def test_recontruct_abstract():
    inverted_index={
        "Machine":[0],
        "learning":[1],
        "is":[2],
        "useful":[3]
    }

    result=reconstruct_abstract(inverted_index)

    assert result=="Machine learning is useful"


def test_reconstruct_abstract_returns_none():
    assert reconstruct_abstract(None) is None
    assert reconstruct_abstract({}) is None


def test_get_abstract_by_doi():
    response=MagicMock()

    response.status_code=200
    response.json.return_value={
            "abstract_inverted_index": {
            "Machine": [0],
            "learning": [1],
            "works": [2],
        }
    }

    with patch(
        "shodak.research.openalex.httpx.get",
        return_value=response
    ):
        result=get_abstract_by_doi("10.1234/test")

    assert result=="Machine learning works"


def test_openalex_404_returns_none():
    response=MagicMock()

    response.status_code=404

    with patch(
        "shodak.research.openalex.httpx.get",
        return_value=response
    ):
        result=get_abstract_by_doi("10.1234/missing")

    assert result is None