from app.domain.cred_score import CredScoreCalculator


def test_cred_score_is_none_for_uncertain_decision():
    calculator = CredScoreCalculator()

    result = calculator.compute(
        decision="uncertain",
        confidence=None,
        estimated_age=None,
        threshold=18,
        margin=2,
    )

    assert result["score"] == 0.0
    assert result["level"] == "none"
    assert result["factors"]["model_confidence"] == "none"
    assert result["factors"]["threshold_separation"] == "none"


def test_cred_score_is_high_for_confident_decision_far_from_threshold():
    calculator = CredScoreCalculator()

    result = calculator.compute(
        decision="match",
        confidence=0.95,
        estimated_age=30,
        threshold=18,
        margin=2,
    )

    assert result["score"] >= 0.85
    assert result["level"] == "high"
    assert result["factors"]["model_confidence"] == "high"
    assert result["factors"]["threshold_separation"] == "high"


def test_cred_score_does_not_expose_raw_age_or_threshold_distance():
    calculator = CredScoreCalculator()

    result = calculator.compute(
        decision="match",
        confidence=0.95,
        estimated_age=30,
        threshold=18,
        margin=2,
    )

    assert "estimated_age" not in result
    assert "threshold_distance" not in result["factors"]
