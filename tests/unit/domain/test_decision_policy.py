from app.domain.decision.policy import DecisionPolicy


def test_decision_policy_returns_match():
    policy = DecisionPolicy()

    decision, reason = policy.compute(
        age=25,
        signal_quality_score=0.8,
        threshold=18,
        margin=2,
        signal_quality_threshold=0.7,
    )

    assert decision == "match"
    assert reason is None


def test_decision_policy_returns_no_match():
    policy = DecisionPolicy()

    decision, reason = policy.compute(
        age=14,
        signal_quality_score=0.8,
        threshold=18,
        margin=2,
        signal_quality_threshold=0.7,
    )

    assert decision == "no_match"
    assert reason is None


def test_decision_policy_returns_uncertain_for_low_signal_quality():
    policy = DecisionPolicy()

    decision, reason = policy.compute(
        age=25,
        signal_quality_score=0.5,
        threshold=18,
        margin=2,
        signal_quality_threshold=0.7,
    )

    assert decision == "uncertain"
    assert reason == "low_signal_quality"


def test_decision_policy_returns_uncertain_for_threshold_uncertain():
    policy = DecisionPolicy()

    decision, reason = policy.compute(
        age=18,
        signal_quality_score=0.8,
        threshold=18,
        margin=2,
        signal_quality_threshold=0.7,
    )

    assert decision == "uncertain"
    assert reason == "threshold_uncertain"
