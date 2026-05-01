class DecisionPolicy:
    """
    Computes a privacy-first threshold decision from internal model output.

    The estimated age is used only inside the service.
    It must not be exposed in the public response.
    """

    def compute(
        self,
        age: float,
        confidence: float,
        threshold: int,
        margin: int,
        confidence_threshold: float,
    ) -> tuple[str, str | None]:
        """
        Return decision and optional rejection reason.

        Decisions:
        - match: the internal estimate is safely above the requested minimum age.
        - no_match: the internal estimate is safely below the requested minimum age.
        - uncertain: the system cannot decide with enough confidence.
        """
        if confidence < confidence_threshold:
            return "uncertain", "low_confidence"

        lower_bound = threshold - margin
        upper_bound = threshold + margin

        if lower_bound <= age <= upper_bound:
            return "uncertain", "threshold_uncertain"

        if age > upper_bound:
            return "match", None

        return "no_match", None
