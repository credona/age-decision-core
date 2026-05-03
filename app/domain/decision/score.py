from app.domain.decision.constants import (
    DECISION_UNCERTAIN,
    SCORE_LEVEL_HIGH,
    SCORE_LEVEL_LOW,
    SCORE_LEVEL_MEDIUM,
    SCORE_LEVEL_NONE,
)
from app.domain.scoring.policy import AgeScoringPolicy, default_age_scoring_policy


class CredScoreCalculator:
    """
    Computes a normalized credibility score for an age threshold decision.

    The score does not expose raw estimated age, raw signal_quality_score, or threshold
    distance. It only exposes categorical factors to preserve the privacy-first
    public contract.
    """

    def __init__(self, scoring_policy: AgeScoringPolicy | None = None):
        self.scoring_policy = scoring_policy or default_age_scoring_policy()

    def compute(
        self,
        decision: str,
        signal_quality_score: float | None,
        internal_estimate: float | None,
        threshold: int | None = None,
        margin: int | None = None,
    ) -> dict:
        policy = self.scoring_policy
        threshold_value = threshold if threshold is not None else policy.age_threshold
        margin_value = margin if margin is not None else policy.age_margin

        if (
            decision == DECISION_UNCERTAIN
            or signal_quality_score is None
            or internal_estimate is None
        ):
            return {
                "score": 0.0,
                "level": SCORE_LEVEL_NONE,
                "factors": {
                    "signal_quality": self._signal_quality_level(signal_quality_score),
                    "threshold_separation": SCORE_LEVEL_NONE,
                },
            }

        distance = abs(internal_estimate - threshold_value)

        if margin_value <= 0:
            distance_factor = 1.0
        else:
            denominator = margin_value * policy.separation_margin_multiplier
            distance_factor = min(distance / denominator, 1.0)

        score = round(
            (signal_quality_score * policy.signal_quality_weight)
            + (distance_factor * policy.threshold_separation_weight),
            4,
        )

        return {
            "score": score,
            "level": self._score_level(score),
            "factors": {
                "signal_quality": self._signal_quality_level(signal_quality_score),
                "threshold_separation": self._separation_level(distance_factor),
            },
        }

    def _score_level(self, score: float) -> str:
        if score >= 0.85:
            return SCORE_LEVEL_HIGH

        if score >= 0.65:
            return SCORE_LEVEL_MEDIUM

        if score > 0:
            return SCORE_LEVEL_LOW

        return SCORE_LEVEL_NONE

    def _signal_quality_level(self, signal_quality_score: float | None) -> str:
        if signal_quality_score is None:
            return SCORE_LEVEL_NONE

        if signal_quality_score >= 0.85:
            return SCORE_LEVEL_HIGH

        if signal_quality_score >= 0.65:
            return SCORE_LEVEL_MEDIUM

        if signal_quality_score > 0:
            return SCORE_LEVEL_LOW

        return SCORE_LEVEL_NONE

    def _separation_level(self, distance_factor: float) -> str:
        if distance_factor >= 0.85:
            return SCORE_LEVEL_HIGH

        if distance_factor >= 0.5:
            return SCORE_LEVEL_MEDIUM

        if distance_factor > 0:
            return SCORE_LEVEL_LOW

        return SCORE_LEVEL_NONE
