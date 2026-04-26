from app.domain.cred_score import CredScoreCalculator


def test_cred_score_is_none_for_unknown_decision():
    calculator = CredScoreCalculator()

    result = calculator.compute(
        decision="unknown",
        confidence=None,
        estimated_age=None,
        threshold=18,
        margin=2,
    )

    assert result["score"] == 0.0
    assert result["level"] == "none"


def test_cred_score_is_high_for_confident_decision_far_from_threshold():
    calculator = CredScoreCalculator()

    result = calculator.compute(
        decision="adult",
        confidence=0.95,
        estimated_age=30,
        threshold=18,
        margin=2,
    )

    assert result["score"] >= 0.85
    assert result["level"] == "high"