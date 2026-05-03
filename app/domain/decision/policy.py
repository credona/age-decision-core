from app.domain.decision.constants import (
    DECISION_MATCH,
    DECISION_NO_MATCH,
    DECISION_UNCERTAIN,
    REJECTION_LOW_SIGNAL_QUALITY,
    REJECTION_THRESHOLD_UNCERTAIN,
)


class DecisionPolicy:
    """
    Computes a privacy-first threshold decision from internal model output.

    The estimated age is used only inside the service.
    It must not be exposed in the public response.
    """

    def compute(
        self,
        age: float,
        signal_quality_score: float,
        threshold: int,
        margin: int,
        signal_quality_threshold: float,
    ) -> tuple[str, str | None]:
        """
        Return decision and optional rejection reason.

        Decisions:
        - match: the internal estimate is safely above the requested minimum age.
        - no_match: the internal estimate is safely below the requested minimum age.
        - uncertain: the system cannot decide with enough signal_quality_score.
        """
        if signal_quality_score < signal_quality_threshold:
            return DECISION_UNCERTAIN, REJECTION_LOW_SIGNAL_QUALITY

        lower_bound = threshold - margin
        upper_bound = threshold + margin

        if lower_bound <= age <= upper_bound:
            return DECISION_UNCERTAIN, REJECTION_THRESHOLD_UNCERTAIN

        if age > upper_bound:
            return DECISION_MATCH, None

        return DECISION_NO_MATCH, None
