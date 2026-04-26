class DecisionPolicy:
    """
    Computes the final age decision from model output and request policy.
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
        """
        if confidence < confidence_threshold:
            return "unknown", "low_confidence"

        lower_bound = threshold - margin
        upper_bound = threshold + margin

        if lower_bound <= age <= upper_bound:
            return "unknown", "age_uncertain"

        if age > upper_bound:
            return "adult", None

        return "minor", None