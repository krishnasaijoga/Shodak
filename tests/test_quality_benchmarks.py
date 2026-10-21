from shodak.evaluation.benchmarks import load_quality_benchmarks


def test_quality_benchmarks_load():
    benchmarks = load_quality_benchmarks()
    assert len(benchmarks) >= 5

    names = {benchmark["name"] for benchmark in benchmarks}

    assert "well_grounded_blog" in names
    assert "unsupported_claims" in names
    assert "wrong_citation" in names
    assert "missing_blog_sections" in names
    assert "weak_research" in names
