from dataclasses import dataclass

DEFAULT_AGE_SCORING_POLICY_ID = "credona.age.threshold-margin.v1"


@dataclass(frozen=True)
class AgeScoringPolicy:
    policy_id: str
    age_threshold: int
    age_margin: int
    signal_quality_threshold: float
    signal_quality_weight: float
    threshold_separation_weight: float
    separation_margin_multiplier: int

    def validate(self) -> None:
        if not self.policy_id:
            raise ValueError("policy_id is required")

        if self.age_threshold <= 0:
            raise ValueError("age_threshold must be positive")

        if self.age_margin < 0:
            raise ValueError("age_margin must be greater than or equal to zero")

        if not 0 <= self.signal_quality_threshold <= 1:
            raise ValueError("signal_quality_threshold must be between 0 and 1")

        if not 0 <= self.signal_quality_weight <= 1:
            raise ValueError("signal_quality_weight must be between 0 and 1")

        if not 0 <= self.threshold_separation_weight <= 1:
            raise ValueError("threshold_separation_weight must be between 0 and 1")

        if round(self.signal_quality_weight + self.threshold_separation_weight, 6) != 1:
            raise ValueError("scoring weights must sum to 1")

        if self.separation_margin_multiplier <= 0:
            raise ValueError("separation_margin_multiplier must be positive")


def default_age_scoring_policy() -> AgeScoringPolicy:
    policy = AgeScoringPolicy(
        policy_id=DEFAULT_AGE_SCORING_POLICY_ID,
        age_threshold=18,
        age_margin=2,
        signal_quality_threshold=0.7,
        signal_quality_weight=0.7,
        threshold_separation_weight=0.3,
        separation_margin_multiplier=3,
    )
    policy.validate()
    return policy
