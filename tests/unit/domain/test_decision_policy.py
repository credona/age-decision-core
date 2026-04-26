from app.domain.decision_policy import DecisionPolicy


def test_decision_policy_returns_adult():
    policy = DecisionPolicy()

    decision, reason = policy.compute(
        age=25,
        confidence=0.8,
        threshold=18,
        margin=2,
        confidence_threshold=0.7,
    )

    assert decision == "adult"
    assert reason is None


def test_decision_policy_returns_minor():
    policy = DecisionPolicy()

    decision, reason = policy.compute(
        age=14,
        confidence=0.8,
        threshold=18,
        margin=2,
        confidence_threshold=0.7,
    )

    assert decision == "minor"
    assert reason is None


def test_decision_policy_returns_unknown_for_low_confidence():
    policy = DecisionPolicy()

    decision, reason = policy.compute(
        age=25,
        confidence=0.5,
        threshold=18,
        margin=2,
        confidence_threshold=0.7,
    )

    assert decision == "unknown"
    assert reason == "low_confidence"


def test_decision_policy_returns_unknown_for_age_uncertain():
    policy = DecisionPolicy()

    decision, reason = policy.compute(
        age=18,
        confidence=0.8,
        threshold=18,
        margin=2,
        confidence_threshold=0.7,
    )

    assert decision == "unknown"
    assert reason == "age_uncertain"