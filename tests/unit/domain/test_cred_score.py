from app.domain.decision.score import CredScoreCalculator


def test_cred_score_is_none_for_uncertain_decision():
    calculator = CredScoreCalculator()

    result = calculator.compute(
        decision="uncertain",
        signal_quality_score=None,
        internal_estimate=None,
        threshold=18,
        margin=2,
    )

    assert result["score"] == 0.0
    assert result["level"] == "none"
    assert result["factors"]["signal_quality"] == "none"
    assert result["factors"]["threshold_separation"] == "none"


def test_cred_score_is_high_for_confident_decision_far_from_threshold():
    calculator = CredScoreCalculator()

    result = calculator.compute(
        decision="match",
        signal_quality_score=0.95,
        internal_estimate=30,
        threshold=18,
        margin=2,
    )

    assert result["score"] >= 0.85
    assert result["level"] == "high"
    assert result["factors"]["signal_quality"] == "high"
    assert result["factors"]["threshold_separation"] == "high"


def test_cred_score_does_not_expose_raw_age_or_threshold_distance():
    calculator = CredScoreCalculator()

    result = calculator.compute(
        decision="match",
        signal_quality_score=0.95,
        internal_estimate=30,
        threshold=18,
        margin=2,
    )

    assert "internal_estimate" not in result
    assert "threshold_distance" not in result["factors"]
