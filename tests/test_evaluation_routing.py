from shodak.evaluation.scorecard import EvaluationScorecard
from shodak.graph.routing import route_after_evaluation


def test_low_quality_routes_to_revision():
    scorecard = EvaluationScorecard(
        grounding_score=0.5,
        citation_correctness_score=0.6,
        hallucination_safety_score=0.5,
        style_similarity_score=0.8,
        format_compliance_score=1.0,
        research_quality_score=0.8,
        overall_quality_score=0.7,
    )
    state = {"evaluation_scorecard": scorecard, "revision_count": 0}
    assert route_after_evaluation(state) == "revise"


def test_good_quality_routes_to_render():
    scorecard = EvaluationScorecard(
        grounding_score=0.9,
        citation_correctness_score=0.9,
        hallucination_safety_score=0.9,
        style_similarity_score=0.8,
        format_compliance_score=1.0,
        research_quality_score=0.8,
        overall_quality_score=0.88,
    )
    state = {"evaluation_scorecard": scorecard, "revision_count": 0}
    assert route_after_evaluation(state) == "render"


def test_revision_limit_soutes_to_render():
    scorecard = EvaluationScorecard(
        grounding_score=0.3,
        citation_correctness_score=0.3,
        hallucination_safety_score=0.3,
        style_similarity_score=0.5,
        format_compliance_score=0.5,
        research_quality_score=0.5,
        overall_quality_score=0.4,
    )
    state = {"evaluation_scorecard": scorecard, "revision_count": 3}
    assert route_after_evaluation(state) == "render"
