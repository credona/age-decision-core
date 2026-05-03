from app.domain.decision.constants import (
    DECISION_MATCH,
    DECISION_NO_MATCH,
    DECISION_UNCERTAIN,
    REJECTION_LOW_SIGNAL_QUALITY,
    REJECTION_THRESHOLD_UNCERTAIN,
)
from app.domain.scoring.policy import AgeScoringPolicy, default_age_scoring_policy


class DecisionPolicy:
    """
    Computes a privacy-first threshold decision from internal model output.

    The estimated age is used only inside the service.
    It must not be exposed in the public response.
    """

    def __init__(self, scoring_policy: AgeScoringPolicy | None = None):
        self.scoring_policy = scoring_policy or default_age_scoring_policy()

    def compute(
        self,
        age: float,
        signal_quality_score: float,
        threshold: int | None = None,
        margin: int | None = None,
        signal_quality_threshold: float | None = None,
    ) -> tuple[str, str | None]:
        policy = self.scoring_policy

        threshold_value = threshold if threshold is not None else policy.age_threshold
        margin_value = margin if margin is not None else policy.age_margin
        signal_quality_threshold_value = (
            signal_quality_threshold
            if signal_quality_threshold is not None
            else policy.signal_quality_threshold
        )

        if signal_quality_score < signal_quality_threshold_value:
            return DECISION_UNCERTAIN, REJECTION_LOW_SIGNAL_QUALITY

        lower_bound = threshold_value - margin_value
        upper_bound = threshold_value + margin_value

        if lower_bound <= age <= upper_bound:
            return DECISION_UNCERTAIN, REJECTION_THRESHOLD_UNCERTAIN

        if age > upper_bound:
            return DECISION_MATCH, None

        return DECISION_NO_MATCH, None
