import pytest

from app.domain.scoring.policy import AgeScoringPolicy, default_age_scoring_policy


def test_default_age_scoring_policy_is_valid_and_versioned():
    policy = default_age_scoring_policy()

    assert policy.policy_id == "credona.age.threshold-margin.v1"
    assert policy.age_threshold == 18
    assert policy.age_margin == 2
    assert policy.signal_quality_threshold == 0.7
    assert policy.signal_quality_weight == 0.7
    assert policy.threshold_separation_weight == 0.3
    assert policy.separation_margin_multiplier == 3


def test_age_scoring_policy_rejects_invalid_weights():
    policy = AgeScoringPolicy(
        policy_id="credona.age.invalid.v1",
        age_threshold=18,
        age_margin=2,
        signal_quality_threshold=0.7,
        signal_quality_weight=0.8,
        threshold_separation_weight=0.3,
        separation_margin_multiplier=3,
    )

    with pytest.raises(ValueError, match="weights"):
        policy.validate()


def test_age_scoring_policy_rejects_invalid_signal_quality_threshold():
    policy = AgeScoringPolicy(
        policy_id="credona.age.invalid.v1",
        age_threshold=18,
        age_margin=2,
        signal_quality_threshold=1.2,
        signal_quality_weight=0.7,
        threshold_separation_weight=0.3,
        separation_margin_multiplier=3,
    )

    with pytest.raises(ValueError, match="signal_quality_threshold"):
        policy.validate()
